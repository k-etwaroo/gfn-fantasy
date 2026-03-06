"""
GFN Fantasy League — Data Pipeline
Pulls all historical data from Yahoo Fantasy API (2011–2025)
and saves structured JSON files ready for the dashboard.

Usage:
    python3 fetch_gfn_data.py              # Pull all seasons
    python3 fetch_gfn_data.py --year 2024  # Pull a single season
    python3 fetch_gfn_data.py --dry-run    # Test auth only
    python3 fetch_gfn_data.py --build      # Rebuild dashboard_data.json only
"""

import os
import json
import argparse
import time
import requests
import base64
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from owner_map import get_owner, GUID_TO_OWNER, ACTIVE_OWNERS

load_dotenv(Path(__file__).parent / '.env')

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
CLIENT_ID      = os.getenv("YAHOO_CLIENT_ID")
CLIENT_SECRET  = os.getenv("YAHOO_CLIENT_SECRET")
ACCESS_TOKEN   = os.getenv("YAHOO_ACCESS_TOKEN")
REFRESH_TOKEN  = os.getenv("YAHOO_REFRESH_TOKEN")
LEAGUE_ID      = os.getenv("YAHOO_LEAGUE_ID")
SEASON_START   = int(os.getenv("SEASON_START", 2011))
SEASON_END     = int(os.getenv("SEASON_END", 2025))

OUTPUT_DIR = Path(__file__).parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / "seasons").mkdir(exist_ok=True)

TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
BASE_URL  = "https://fantasysports.yahooapis.com/fantasy/v2"

_access_token = ACCESS_TOKEN

LEAGUE_KEYS = {
    2011: "257.l.114705",
    2012: "273.l.241229",
    2013: "314.l.214310",
    2014: "331.l.145833",
    2015: "348.l.225929",
    2016: "359.l.285789",
    2017: "371.l.13839",
    2018: "380.l.181541",
    2019: "390.l.650144",
    2020: "399.l.596553",
    2021: "406.l.185056",
    2022: "414.l.321722",
    2023: "423.l.132892",
    2024: "449.l.62560",
    2025: "461.l.23054",
}


# ─────────────────────────────────────────────
# TOKEN REFRESH
# ─────────────────────────────────────────────
def refresh_access_token():
    global _access_token
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    resp = requests.post(TOKEN_URL,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type":    "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            "redirect_uri":  "https://k-etwaroo.github.io/gfn-fantasy",
        }
    )
    resp.raise_for_status()
    data = resp.json()
    _access_token = data["access_token"]
    print("  ✓ Token refreshed.")
    return _access_token


# ─────────────────────────────────────────────
# API REQUEST
# ─────────────────────────────────────────────
def yahoo_get(path, params=None, retry=True):
    global _access_token
    url = f"{BASE_URL}{path}"
    headers = {"Authorization": f"Bearer {_access_token}"}
    default_params = {"format": "json"}
    if params:
        default_params.update(params)

    resp = requests.get(url, headers=headers, params=default_params)

    if resp.status_code == 401 and retry:
        print("  ⚠ Token expired — refreshing...")
        refresh_access_token()
        return yahoo_get(path, params, retry=False)

    if resp.status_code != 200:
        print(f"  ✗ API error {resp.status_code}: {path}")
        print(f"    {resp.text[:300]}")
        return None

    return resp.json()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def get_league_key(year):
    key = LEAGUE_KEYS.get(year)
    if not key:
        raise ValueError(f"No league key for year {year}")
    return key


def safe_save(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ Saved → {filepath}")


def flatten(list_of_dicts):
    """Flatten Yahoo's list-of-dicts structure into one dict."""
    result = {}
    for item in list_of_dicts:
        if isinstance(item, dict):
            result.update(item)
    return result


# ─────────────────────────────────────────────
# FETCH FUNCTIONS
# ─────────────────────────────────────────────
def fetch_league_meta(year):
    key  = get_league_key(year)
    data = yahoo_get(f"/league/{key}/metadata")
    if not data:
        return None
    league = data["fantasy_content"]["league"][0]
    return {
        "year":          year,
        "league_key":    key,
        "name":          league.get("name"),
        "num_teams":     league.get("num_teams"),
        "current_week":  league.get("current_week"),
        "start_week":    league.get("start_week"),
        "end_week":      league.get("end_week"),
        "playoff_start": league.get("start_week_of_playoffs"),
    }


def fetch_standings(year):
    key  = get_league_key(year)
    data = yahoo_get(f"/league/{key}/standings")
    if not data:
        return []

    teams_raw = data["fantasy_content"]["league"][1]["standings"][0]["teams"]
    standings = []

    for i in range(teams_raw["count"]):
        team_data = teams_raw[str(i)]["team"]
        info      = flatten(team_data[0])

        # standings data can be at index 1 or 2 depending on year
        standing_block = None
        for block in team_data[1:]:
            if isinstance(block, dict) and "team_standings" in block:
                standing_block = block["team_standings"]
                break

        if not standing_block:
            # fallback: try team_points or empty
            standing_block = {}

        outcome = standing_block.get("outcome_totals", {})
        team_name = info.get("name", "")
        managers_block = next(
            (d.get("managers") for d in team_data[0] if isinstance(d, dict) and "managers" in d), []
        )
        guid = managers_block[0]["manager"].get("guid") if managers_block else None
        _, owner = get_owner(team_name=team_name, guid=guid)

        standings.append({
            "team_key":       info.get("team_key", ""),
            "name":           team_name,
            "owner":          owner,
            "guid":           guid,
            "rank":           int(standing_block.get("rank", 0)) if standing_block.get("rank") else None,
            "wins":           int(outcome.get("wins", 0)),
            "losses":         int(outcome.get("losses", 0)),
            "ties":           int(outcome.get("ties", 0)),
            "points_for":     float(standing_block.get("points_for", 0)),
            "points_against": float(standing_block.get("points_against", 0)),
            "playoff_seed":   standing_block.get("playoff_seed"),
        })

    standings.sort(key=lambda x: x["rank"] or 99)
    return standings


def fetch_matchups(year):
    key  = get_league_key(year)
    meta = fetch_league_meta(year)
    if not meta:
        return []

    start_week = int(meta.get("start_week", 1))
    end_week   = int(meta.get("end_week", 16))

    all_matchups = []
    for week in range(start_week, end_week + 1):
        data = yahoo_get(f"/league/{key}/scoreboard;week={week}")
        if not data:
            continue

        try:
            matchups_raw = data["fantasy_content"]["league"][1]["scoreboard"]["0"]["matchups"]
        except (KeyError, TypeError):
            continue

        for i in range(matchups_raw.get("count", 0)):
            m            = matchups_raw[str(i)]["matchup"]
            week_matchup = {
                "week":        week,
                "is_playoffs": m.get("is_playoffs", "0") == "1",
                "teams":       []
            }
            teams = m["0"]["teams"]
            for j in range(teams.get("count", 0)):
                t     = teams[str(j)]["team"]
                info  = flatten(t[0])
                score = t[1].get("team_points", {}) if len(t) > 1 else {}
                team_name = info.get("name", "")
                mgr_block = next((d.get("managers") for d in t[0] if isinstance(d, dict) and "managers" in d), [])
                guid      = mgr_block[0]["manager"].get("guid") if mgr_block else None
                _, owner  = get_owner(team_name=team_name, guid=guid)
                week_matchup["teams"].append({
                    "team_key": info.get("team_key", ""),
                    "name":     team_name,
                    "owner":    owner,
                    "points":   float(score.get("total", 0)),
                })
            all_matchups.append(week_matchup)

        time.sleep(0.3)

    return all_matchups


def fetch_season(year):
    print(f"\n{'─'*50}")
    print(f"  Fetching {year} season...")
    print(f"{'─'*50}")

    season_data = {"year": year}

    print("  → League metadata...")
    meta = fetch_league_meta(year)
    if not meta:
        print(f"  ✗ Could not fetch league for {year} — skipping.")
        return None
    season_data["meta"] = meta

    print("  → Standings...")
    season_data["standings"] = fetch_standings(year)

    print("  → Weekly matchups (this may take a moment)...")
    season_data["matchups"] = fetch_matchups(year)

    path = OUTPUT_DIR / "seasons" / f"{year}.json"
    safe_save(path, season_data)
    return season_data


# ─────────────────────────────────────────────
# LUCK INDEX
# ─────────────────────────────────────────────
def compute_luck_index(season_data):
    matchups = [m for m in season_data.get("matchups", []) if not m["is_playoffs"]]

    weekly_scores = {}
    actual_wins   = {}

    for m in matchups:
        if len(m["teams"]) < 2:
            continue
        t0, t1 = m["teams"][0], m["teams"][1]
        for t in [t0, t1]:
            weekly_scores.setdefault(t["owner"], []).append(t["points"])
        if t0["points"] > t1["points"]:
            actual_wins[t0["owner"]] = actual_wins.get(t0["owner"], 0) + 1
        elif t1["points"] > t0["points"]:
            actual_wins[t1["owner"]] = actual_wins.get(t1["owner"], 0) + 1

    expected_wins = {k: 0.0 for k in weekly_scores}
    num_weeks     = max(len(v) for v in weekly_scores.values()) if weekly_scores else 0

    for week_idx in range(num_weeks):
        scores_this_week = {
            k: v[week_idx] for k, v in weekly_scores.items() if week_idx < len(v)
        }
        all_scores = list(scores_this_week.values())
        n          = len(all_scores)
        for owner, score in scores_this_week.items():
            beats = sum(1 for s in all_scores if score > s) / max(n - 1, 1)
            expected_wins[owner] += beats

    luck_results = []
    for owner in weekly_scores:
        a = actual_wins.get(owner, 0)
        e = round(expected_wins.get(owner, 0), 2)
        luck_results.append({
            "owner":         owner,
            "actual_wins":   a,
            "expected_wins": e,
            "luck_score":    round(a - e, 2),
        })

    luck_results.sort(key=lambda x: x["luck_score"], reverse=True)
    return luck_results


# ─────────────────────────────────────────────
# POWER RANKINGS
# ─────────────────────────────────────────────
def compute_power_rankings(season_data, top_n_weeks=4):
    matchups        = [m for m in season_data.get("matchups", []) if not m["is_playoffs"]]
    weeks_by_number = {}
    for m in matchups:
        weeks_by_number.setdefault(m["week"], []).append(m)

    team_history = {}
    for week in sorted(weeks_by_number.keys()):
        for m in weeks_by_number[week]:
            if len(m["teams"]) < 2:
                continue
            t0, t1 = m["teams"][0], m["teams"][1]
            w0     = 1 if t0["points"] > t1["points"] else 0
            team_history.setdefault(t0["owner"], []).append({"week": week, "pts": t0["points"], "win": w0})
            team_history.setdefault(t1["owner"], []).append({"week": week, "pts": t1["points"], "win": 1 - w0})

    all_pts     = [g["pts"] for games in team_history.values() for g in games]
    avg_pts_all = sum(all_pts) / len(all_pts) if all_pts else 1

    rankings = []
    for owner, games in team_history.items():
        recent  = games[-top_n_weeks:]
        win_pct = sum(g["win"] for g in recent) / len(recent) if recent else 0
        avg_pts = sum(g["pts"] for g in recent) / len(recent) if recent else 0
        score   = round((win_pct * 0.6 + (avg_pts / avg_pts_all) * 0.4) * 100, 1)
        rankings.append({"owner": owner, "pr_score": score})

    rankings.sort(key=lambda x: x["pr_score"], reverse=True)
    for i, r in enumerate(rankings):
        r["rank"] = i + 1

    return rankings


# ─────────────────────────────────────────────
# BUILD DASHBOARD DATA
# ─────────────────────────────────────────────
def build_dashboard_data():
    print("\n📊 Building dashboard_data.json...")

    all_seasons = []
    for year in range(SEASON_START, SEASON_END + 1):
        path = OUTPUT_DIR / "seasons" / f"{year}.json"
        if path.exists():
            with open(path) as f:
                all_seasons.append(json.load(f))
        else:
            print(f"  ⚠ Missing {year}.json — skipping")

    if not all_seasons:
        print("  ✗ No season data found.")
        return

    # Champions
    champions = []
    for s in all_seasons:
        top = next((t for t in s.get("standings", []) if t.get("rank") == 1), None)
        if top:
            champions.append({
                "year":    s["year"],
                "team":    top["name"],
                "owner":   top["owner"],
                "wins":    top["wins"],
                "losses":  top["losses"],
                "pts_for": top["points_for"],
            })

    # All-time owner stats (keyed by owner name)
    owner_stats = {name: {"wins": 0, "losses": 0, "pts_for": 0.0,
                           "pts_against": 0.0, "titles": 0, "seasons": 0,
                           "playoff_appearances": 0}
                   for name in set(GUID_TO_OWNER.values())}

    for s in all_seasons:
        num_teams    = len(s.get("standings", []))
        playoff_spots = max(4, num_teams // 3)
        for t in s.get("standings", []):
            owner = t.get("owner")
            if not owner or owner not in owner_stats:
                continue
            owner_stats[owner]["wins"]        += t["wins"]
            owner_stats[owner]["losses"]      += t["losses"]
            owner_stats[owner]["pts_for"]     += t["points_for"]
            owner_stats[owner]["pts_against"] += t["points_against"]
            owner_stats[owner]["seasons"]     += 1
            if t.get("rank") == 1:
                owner_stats[owner]["titles"]  += 1
            if t.get("playoff_seed") and int(t["playoff_seed"]) <= playoff_spots:
                owner_stats[owner]["playoff_appearances"] += 1

    # Luck index
    luck_by_season = {}
    luck_alltime   = {name: [] for name in set(GUID_TO_OWNER.values())}

    for s in all_seasons:
        luck = compute_luck_index(s)
        luck_by_season[s["year"]] = luck
        for r in luck:
            owner = r["owner"]
            if owner in luck_alltime:
                luck_alltime[owner].append(r["luck_score"])

    luck_summary = sorted([
        {
            "owner":   owner,
            "avg":     round(sum(scores) / len(scores), 2) if scores else 0,
            "total":   round(sum(scores), 2) if scores else 0,
            "seasons": len(scores),
        }
        for owner, scores in luck_alltime.items() if scores
    ], key=lambda x: x["total"], reverse=True)

    # Power rankings from latest season
    power_rankings = compute_power_rankings(all_seasons[-1])

    dashboard = {
        "generated_at":   datetime.now().isoformat(),
        "seasons_count":  len(all_seasons),
        "champions":      champions,
        "owner_stats":    owner_stats,
        "luck_by_season": luck_by_season,
        "luck_summary":   luck_summary,
        "power_rankings": power_rankings,
    }

    out = OUTPUT_DIR / "dashboard_data.json"
    safe_save(out, dashboard)
    print(f"\n✅ Dashboard data ready → {out}")
    return dashboard


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="GFN Fantasy Data Pipeline")
    parser.add_argument("--year",    type=int, help="Fetch a single season year")
    parser.add_argument("--dry-run", action="store_true", help="Test auth only")
    parser.add_argument("--build",   action="store_true", help="Rebuild dashboard_data.json only")
    parser.add_argument("--refetch", action="store_true", help="Re-fetch all seasons even if cached")
    args = parser.parse_args()

    missing = [k for k, v in {
        "YAHOO_CLIENT_ID":     CLIENT_ID,
        "YAHOO_CLIENT_SECRET": CLIENT_SECRET,
        "YAHOO_ACCESS_TOKEN":  ACCESS_TOKEN,
        "YAHOO_LEAGUE_ID":     LEAGUE_ID,
    }.items() if not v]

    if missing:
        print(f"✗ Missing env vars: {', '.join(missing)}")
        return

    if args.dry_run:
        print("🔐 Testing auth...")
        data = yahoo_get("/game/nfl")
        if data:
            print("✅ Auth successful! Yahoo Fantasy API is responding.")
        else:
            print("✗ Auth failed. Check your tokens in .env")
        return

    if args.build:
        build_dashboard_data()
        return

    if args.year:
        # Always re-fetch when a specific year is requested
        path = OUTPUT_DIR / "seasons" / f"{args.year}.json"
        if path.exists():
            path.unlink()
        fetch_season(args.year)
        build_dashboard_data()
    else:
        print(f"🏈 GFN Data Pipeline — Fetching {SEASON_START}–{SEASON_END}")
        print(f"   League ID: {LEAGUE_ID}\n")
        for year in range(SEASON_START, SEASON_END + 1):
            path = OUTPUT_DIR / "seasons" / f"{year}.json"
            if path.exists() and not args.refetch:
                print(f"  ⏭  {year} already cached — skipping")
                continue
            fetch_season(year)
            time.sleep(1)
        build_dashboard_data()

    print("\n🏆 All done! Check data/dashboard_data.json")


if __name__ == "__main__":
    main()
