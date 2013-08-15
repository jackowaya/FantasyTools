#!/usr/bin/env python

from collections import defaultdict
import sys
import csv

if len(sys.argv) != 3:
  print "Usage: combineLists.py list1 list2"
  sys.exit(2)

# A player looks like
# { name: .., position: .., team: .., rank1: .., rank2: .., rank: .., prk1: .., prk2: .., prk: .., }
players = {}
positionCounts1 = defaultdict(int)
positionCounts2 = defaultdict(int)
TOTAL_COUNT = 200

with open(sys.argv[1], 'r') as f1:
  reader = csv.reader(f1)
  count = 0
  for row in reader:
    if row[1] == "Team":
      continue
    count += 1
    name = row[0]
    team = row[1]
    pos = row[2]
    positionCounts1[pos] += 1
    players[name] = {
      "name": name,
      "team": team,
      "pos": pos,
      "rank1": count,
      "rank2": 0,
      "rank": 0,
      "prk1": positionCounts1[pos],
      "prk2": 0,
      "prk": 0
    }
    if count >= TOTAL_COUNT:
      break

with open(sys.argv[2], 'r') as f1:
  reader = csv.reader(f1)
  count = 0
  for row in reader:
    if row[1] == "Team":
      continue
    count += 1
    name = row[0]
    team = row[1]
    pos = row[2]
    positionCounts2[pos] += 1
    if name in players:
      players[name]["rank2"] = count
      players[name]["prk2"] = positionCounts2[pos]
    else:
      players[name] = {
        "name": name,
        "team": team,
        "pos": pos,
        "rank1": 0,
        "rank2": count,
        "rank": 0,
        "prk1": 0,
        "prk2": positionCounts2[pos],
        "prk": 0
      }
      if count >= TOTAL_COUNT:
        break

results = []
for _, p in players.iteritems():
  if p["rank1"] == 0:
    p["rank1"] = TOTAL_COUNT + 1
  if p["rank2"] == 0:
    p["rank2"] = TOTAL_COUNT + 1
  if p["prk1"] == 0:
    p["prk1"] = positionCounts1[p["pos"]] + 1
  if p["prk2"] == 0:
    p["prk2"] = positionCounts2[p["pos"]] + 1
  p["rank"] = (p["rank1"] + p["rank2"]) / 2
  p["prk"] = (p["prk1"] + p["prk2"]) / 2
  results.append(p)

results = sorted(results, key=lambda p: p["rank"])
print "<table><tr><th>Player</th><th>Team</th><th>Position</th><th>Rank</th><th>James Rank</th><th>Alan Rank</th><th>PRK</th><th>James PRK</th><th>Alan PRK</th></tr>"
count = 0
positionCounts = defaultdict(int)
for p in results:
  count += 1
  name = p["name"]
  team = p["team"]
  pos = p["pos"]
  r = count
  r1 = p["rank1"]
  if r1 == TOTAL_COUNT + 1:
    r1 = "NR"
  else:
    r1 = str(r1)
  r2 = p["rank2"]
  if r2 == TOTAL_COUNT + 1:
    r2 = "NR"
  else:
    r2 = str(r2)
  positionCounts[pos] += 1
  prk = pos + str(positionCounts[pos])
  prk1 = p["prk1"]
  if prk1 == positionCounts1[p["pos"]] + 1:
    prk1 = "NR"
  else:
    prk1 = str(prk1)
  prk2 = p["prk2"]
  if prk2 == positionCounts2[p["pos"]] + 1:
    prk2 = "NR"
  else:
    prk2 = str(prk2)

  print "<tr><td>%s</td><td>%s</td><td>%s</td><td><strong>%d</strong></td><td>%s</td><td>%s</td><td><strong>%s</strong></td><td>%s</td><td>%s</td></tr>" % (name, team, pos, r, r1, r2, prk, prk1, prk2)
print "</table>"
