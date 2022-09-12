print("hello")
from itertools import count
from itertools import combinations
  
import json
from multiprocessing.resource_sharer import stop
exclude_byname = ["mustard","Bell"]
exclude_bypoint = [10.5]
include_byname = ["Ambrose"]
no_wk = 1
no_bat = 3
no_ball = 4
no_allround = 3
teamA = "SL"
teamB = "ENG"
no_players_from_teamA = 5
no_players_from_teamB = 6

def readPlayers():
    # Opening JSON file
    f = open('Dream11\players.json')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    return data["players"]

def exclude_player_byname(data):
    print(len(data))
    for player in exclude_byname:
        if any(x["name"] == player for x in data ):
            for x in data:
                if x["name"] == player:
                    data.remove(x)
        print(len(data))
    verify(data)
    return data

def get_team_count(data,team):
    count = 0
    for x in data:
        if x["team"] == team:
            count =count + 1
    return count

def get_count(data,role):
    count = 0
    for x in data:
        if x["role"] == role:
            count =count + 1
    return count

def verify(data):
    if get_team_count(data,teamA) < 4 :
        print(teamA + "player count less than 4 please change the configs")
    if get_team_count(data,teamB) < 4 :
        print(teamB + "player count less than 4 please change the configs")

def exclude_player_bypoint(data):
    print(len(data))
    for point in exclude_bypoint:
        if any(x["points"] == point for x in data ):
            for x in data:
                if x["points"] == point:
                    data.remove(x)
        print(len(data))
    verify(data)
    return data

def get_points_count(data):
    totalppoints = 0
    for x in data:
        totalppoints = totalppoints + x["points"]
    if totalppoints != 0:
        return totalppoints

    return 101

def check_include(data):
    for name in include_byname:
        if any(x["name"] == name for x in data):
            pass
        else:
            return False
    return True




def letsfilter(probTeam):
    #print(probTeam)
    if get_team_count(probTeam,teamA) > 7 or  get_team_count(probTeam,teamA) < 4 or get_team_count(probTeam,teamA) != no_players_from_teamA:
        return False
    if get_count(probTeam,"keeper") != no_wk:
        return False
    if get_count(probTeam,"batsman") != no_bat:
        return False
    if get_count(probTeam,"bowler") != no_ball:
        return False
    if get_count(probTeam,"allrounder") != no_allround:
        return False
    if get_points_count(probTeam) > 100:
        return False
    if check_include(probTeam) == False:
        return False
    
    
    return True

print(readPlayers())
data1 = exclude_player_byname(readPlayers())
data2 = exclude_player_bypoint(data1)
print(list(combinations(data2,11))[0])
data3 = []
for x in list(combinations(data2,11)) :
    if letsfilter(x):
        data3.append(x)


print(len(data3))