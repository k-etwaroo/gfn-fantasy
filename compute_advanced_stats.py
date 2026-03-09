import json
from pathlib import Path
from collections import defaultdict

seasons_data = {}
for year in range(2011, 2026):
    path = Path(f'data/seasons/{year}.json')
    if path.exists():
        with open(path) as f:
            seasons_data[year] = json.load(f)

def build_bracket(year, data):
    playoff_weeks = [15,16,17] if year >= 2021 else [14,15,16]
    w1, w2, w3 = playoff_weeks
    seeds = {t['owner']: t['rank'] for t in data['standings']}
    champ = next((t['owner'] for t in data['standings'] if t['rank'] == 1), None)

    weeks = {w1: [], w2: [], w3: []}
    for m in data['matchups']:
        if not m.get('is_playoffs'):
            continue
        t1, t2 = m['teams']
        winner = t1['owner'] if t1['points'] > t2['points'] else t2['owner']
        loser = t2['owner'] if winner == t1['owner'] else t1['owner']
        game = {
            "t1": t1['owner'], "t1_pts": t1['points'],
            "t2": t2['owner'], "t2_pts": t2['points'],
            "winner": winner, "loser": loser,
            "margin": round(abs(t1['points'] - t2['points']), 2)
        }
        if m['week'] in weeks:
            weeks[m['week']].append(game)

    # Byes = teams that skipped week 1
    wk1_players = set(p for g in weeks[w1] for p in [g['t1'], g['t2']])
    all_players = set(p for wk in weeks.values() for g in wk for p in [g['t1'], g['t2']])
    byes = all_players - wk1_players

    # Championship bracket only — exclude consolation (seeds 7-12 vs each other)
    con_seeds = {o for o, s in seeds.items() if s >= 7}
    wk1_champ = [g for g in weeks[w1]
                 if not (g['t1'] in con_seeds and g['t2'] in con_seeds)]
    wk1_champ_winners = {g['winner'] for g in wk1_champ}
    champ_teams = byes | wk1_champ_winners

    # Semifinals — championship bracket only
    champ_semis = [g for g in weeks[w2]
                   if g['t1'] in champ_teams or g['t2'] in champ_teams]

    # Finals — find championship game by locating the champion
    finals = {}
    for g in weeks[w3]:
        if champ and champ in [g['t1'], g['t2']]:
            finals['championship'] = g
            break
    # 3rd place = the other game between semifinal losers
    champ_semi_losers = {g['loser'] for g in champ_semis}
    for g in weeks[w3]:
        if g == finals.get('championship'):
            continue
        if g['t1'] in champ_semi_losers and g['t2'] in champ_semi_losers:
            finals['third_place'] = g
            break

    return {
        "byes": sorted(list(byes), key=lambda x: seeds.get(x, 99)),
        "seeds": seeds,
        "round1": sorted(wk1_champ, key=lambda x: seeds.get(x['t1'], 99)),
        "semifinals": champ_semis,
        "finals": finals,
        "champion": champ,
        "weeks": {"round1": w1, "semifinals": w2, "finals": w3}
    }

playoff_brackets = {}
for year, data in seasons_data.items():
    playoff_brackets[year] = build_bracket(year, data)

# Verify 2024
b = playoff_brackets[2024]
print("=== 2024 BRACKET ===")
print(f"Champion: {b['champion']}")
print(f"Byes: {b['byes']}")
print(f"\nRound 1 ({len(b['round1'])} games):")
for g in b['round1']:
    print(f"  {g['t1']} ({g['t1_pts']}) vs {g['t2']} ({g['t2_pts']}) → {g['winner']}")
print(f"\nSemifinals ({len(b['semifinals'])} games):")
for g in b['semifinals']:
    print(f"  {g['t1']} ({g['t1_pts']}) vs {g['t2']} ({g['t2_pts']}) → {g['winner']}")
print(f"\nFinals:")
for k, g in b['finals'].items():
    print(f"  {k}: {g['t1']} ({g['t1_pts']}) vs {g['t2']} ({g['t2_pts']}) → {g['winner']}")

# Schedule strength
schedule_strength = {}
for year, data in seasons_data.items():
    reg_matchups = [m for m in data['matchups'] if not m.get('is_playoffs')]
    opp_scores = defaultdict(list)
    for m in reg_matchups:
        t1, t2 = m['teams']
        opp_scores[t1['owner']].append(t2['points'])
        opp_scores[t2['owner']].append(t1['points'])
    season_ss = []
    for owner, scores in opp_scores.items():
        avg_opp = round(sum(scores) / len(scores), 2) if scores else 0
        season_ss.append({
            "owner": owner,
            "avg_opponent_score": avg_opp,
            "total_opponent_score": round(sum(scores), 2),
            "games": len(scores)
        })
    season_ss.sort(key=lambda x: -x['avg_opponent_score'])
    for i, s in enumerate(season_ss):
        s['schedule_rank'] = i + 1
    schedule_strength[year] = season_ss

# Points vs rank
pts_vs_rank = {}
for year, data in seasons_data.items():
    reg_matchups = [m for m in data['matchups'] if not m.get('is_playoffs')]
    owner_pts = defaultdict(float)
    owner_wins = defaultdict(int)
    for m in reg_matchups:
        t1, t2 = m['teams']
        owner_pts[t1['owner']] += t1['points']
        owner_pts[t2['owner']] += t2['points']
        if t1['points'] > t2['points']:
            owner_wins[t1['owner']] += 1
        else:
            owner_wins[t2['owner']] += 1
    season_data = []
    for team in data['standings']:
        owner = team['owner']
        season_data.append({
            "owner": owner,
            "rank": team['rank'],
            "pts_for": round(owner_pts.get(owner, 0), 1),
            "wins": owner_wins.get(owner, 0)
        })
    pts_vs_rank[year] = season_data

# What-if data
whatif_data = {}
for year, data in seasons_data.items():
    reg_matchups = [m for m in data['matchups'] if not m.get('is_playoffs')]
    owner_weekly = defaultdict(dict)
    all_weekly = defaultdict(list)
    for m in reg_matchups:
        for t in m['teams']:
            owner_weekly[t['owner']][str(m['week'])] = t['points']
            all_weekly[str(m['week'])].append({
                "owner": t['owner'], "points": t['points']
            })
    whatif_data[year] = {
        "owner_weekly_scores": {k: dict(v) for k, v in owner_weekly.items()},
        "all_weekly_scores": dict(all_weekly)
    }

output = {
    "playoff_brackets": {str(k): v for k, v in playoff_brackets.items()},
    "pts_vs_rank": {str(k): v for k, v in pts_vs_rank.items()},
    "schedule_strength": {str(k): v for k, v in schedule_strength.items()},
    "whatif_data": {str(k): v for k, v in whatif_data.items()}
}

with open('data/advanced_stats.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\n✅ Saved data/advanced_stats.json")
