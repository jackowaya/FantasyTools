#!/usr/bin/env python

from collections import defaultdict
import sys
import csv

if len(sys.argv) == 1:
  print "Usage: combineLists.py list1 list2, ..."
  sys.exit(2)

# A player looks like
# { name: .., position: .., team: .., rank: .., prk: .., }
# We index everything from 1, so just add these things
players = [{}]
positionCounts = [{}]
for i in range(1, len(sys.argv)):
  players.append({})
  positionCounts.append(defaultdict(int))

TOTAL_COUNT = 200

for i in range(1, len(sys.argv)):
  with open(sys.argv[i], 'r') as f:
    reader = csv.reader(f)
    count = 0
    for row in reader:
      if row[1] == "Team" or row[1] == "Position":
        continue
      count += 1
      name = row[0]
      team = row[1]
      pos = row[2]
      positionCounts[i][pos] += 1
      players[i][name] = {
        "name": name,
        "team": team,
        "pos": pos,
        "rank": count,
        "prk": positionCounts[i][pos]
        }
      if count >= TOTAL_COUNT:
        break

# convert players to { name: .., position: .., team: .., ranks: {1: .., 2: ..}, rank: .., prks: {1: .., 2:.. }, prk: .., }
results = {}
for i in range(1, len(sys.argv)):
  for _, p in players[i].iteritems():
    if p["name"] in results:
      # Already saw this player, just add some info to them.
      results[p["name"]]["ranks"][i] = p["rank"]
      results[p["name"]]["prks"][i] = p["prk"]
    else:
      # Create this player
      results[p["name"]] = {
        "name": p["name"],
        "team": p["team"],
        "pos": p["pos"],
        "rank": 0,
        "prk": 0,
        "ranks": {i: p["rank"]},
        "prks": {i: p["prk"]}
        }
      

lResults = []
for p in results.values():
  # Calculate rank, prk and add to list results
  for i in range(1, len(sys.argv)):
    # Fill in missing ranks/prks
    if i not in p["ranks"]:
      p["ranks"][i] = TOTAL_COUNT + 1
    if i not in p["prks"]:
      p["prks"][i] = positionCounts[i][p["pos"]] + 1

  for _, v in p["ranks"].iteritems():
    p["rank"] += v
  for _, v in p["prks"].iteritems():
    p["prk"] += v
  p["rank"] /= len(sys.argv) - 1
  p["prk"] /= len(sys.argv) - 1
  lResults.append(p)

lResults = sorted(lResults, key=lambda p: p["rank"])
overallPositionCounts = defaultdict(int)
headerText = "<table><tr><th>Player</th><th>Team</th><th>Position</th><th>Rank</th>"
for i in range(1, len(sys.argv)):
  headerText += "<th>%d Rank</th>" % i
headerText += "<th>PRK</th>"
for i in range(1, len(sys.argv)):
  headerText += "<th>%d PRK</th>" % i
headerText += "</tr>"
print headerText

count = 0
for p in lResults:
  count += 1

  text = "<tr><td>%s</td><td>%s</td><td>%s</td><td><strong>%d</strong></td>" % (p["name"], p["team"], p["pos"], count)
  for i in range(1, len(sys.argv)):
    if p["ranks"][i] == TOTAL_COUNT + 1:
      text += "<td>NR</td>"
    else:
      text += "<td>%d</td>" % p["ranks"][i]
  overallPositionCounts[p["pos"]] += 1
  text += "<td><strong>%s%d</strong></td>" % (p["pos"], overallPositionCounts[p["pos"]])
  for i in range(1, len(sys.argv)):
    if p["prks"][i] == positionCounts[i][p["pos"]] + 1:
      text += "<td>NR</td>"
    else:
      text += "<td>%d</td>" % (p["prks"][i])
  text += "</tr>"
  print text

print "</table>"
