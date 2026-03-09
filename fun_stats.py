import json
from pathlib import Path
from collections import defaultdict

seasons_data = {}
for year in range(2011, 2026):
    path = Path(f'data/seasons/{year}.json')
    if path.exists():
        with open(path) as f:
            seasons_data[year] = json.load(f)

# 1. MOST CONSECUTIVE PLAYOFF APPEARANCES
playoff_by_owner = defaultdict(dict)
for year, data in seasons_data.items():
    for team in data['standings']:
        owner = team.get('owner')
        made_po = team.get('rank', 99) <= 4
        if owner:
            playoff_by_owner[owner][year] = made_po

consec_playoffs = {}
for owner, years in playoff_by_owner.items():
    max_streak = cur = 0
    streak_end = None
    for y in sorted(years.keys()):
        if years[y]:
            cur += 1
            if cur > max_streak:
                max_streak = cur
                streak_end = y
        else:
            cur = 0
    consec_playoffs[owner] = {"streak": max_streak, "streak_end": streak_end}

print("--- CONSECUTIVE PLAYOFF APPEARANCES ---")
for owner, d in sorted(consec_playoffs.items(), key=lambda x: -x[1]["streak"])[:8]:
    print(f"  {owner}: {d['streak']} straight (through {d['streak_end']})")

# 2. MOST POINTS IN A LOSS
worst_losses = []
for year, data in seasons_data.items():
    for m in data.get('matchups', []):
        if m.get('is_playoffs'):
            continue
        teams = m['teams']
        if len(teams) == 2:
            t1, t2 = teams
            loser = t1 if t1['points'] < t2['points'] else t2
            winner = t2 if loser == t1 else t1
            worst_losses.append({
                "owner": loser['owner'], "points": loser['points'],
                "year": year, "week": m['week'],
                "opponent": winner['owner'],
                "opp_points": winner['points']
            })

worst_losses.sort(key=lambda x: -x['points'])
print("\n--- MOST POINTS IN A LOSS ---")
for l in worst_losses[:8]:
    print(f"  {l['owner']}: {l['points']} pts lost to {l['opponent']} ({l['opp_points']}) - {l['year']} Wk {l['week']}")

# 3. BEST REGULAR SEASON RECORD WITHOUT TITLE
heartbreaks = []
for year, data in seasons_data.items():
    champion = next((t['owner'] for t in data['standings'] if t.get('rank') == 1), None)
    for team in data['standings']:
        if team.get('rank', 99) > 1 and team['wins'] >= 9:
            heartbreaks.append({
                "owner": team['owner'], "year": year,
                "wins": team['wins'], "losses": team['losses'],
                "pts_for": team.get("pts_for", team.get("points_for", 0)), "rank": team['rank'],
                "champion": champion
            })

heartbreaks.sort(key=lambda x: (-x['wins'], -x['pts_for']))
print("\n--- BEST RECORD WITHOUT TITLE ---")
for h in heartbreaks[:8]:
    print(f"  {h['owner']}: {h['wins']}-{h['losses']} in {h['year']} (Rank {h['rank']}, {h['pts_for']} pts) - champ was {h['champion']}")

# 4. CURSED LIST
all_titles = defaultdict(int)
for year, data in seasons_data.items():
    champ = next((t['owner'] for t in data['standings'] if t.get('rank') == 1), None)
    if champ:
        all_titles[champ] += 1

active = ["Peter Ott","Lee Bertram","Brian Marois","Tony Bevilaqua","Joshua",
          "Steve Minardi","Kenny Smith","Ed Shively","Kevin Etwaroo",
          "Malcolm Lapone","Christopher Hayes","Jeff Lobdell","Chris Dupay"]

print("\n--- THE CURSED LIST (active, no titles) ---")
for owner in active:
    if all_titles.get(owner, 0) == 0:
        seasons = sum(1 for data in seasons_data.values()
                     for t in data['standings'] if t.get('owner') == owner)
        print(f"  {owner}: {seasons} seasons, 0 titles")

# 5. MOST POINTS IN A LOSS ALL TIME TOP 1
print("\n--- QUICK SUMMARY ---")
print(f"Total matchups analyzed: {len(worst_losses)}")
