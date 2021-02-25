import pandas as pd
import DataGathering.FileHandling as files
import jellyfish

def unifyDates(date: str) -> str:
    if len(date) == 0:
        return "0000/00/00"
    if "." in date:
        date = date.split(".")
    elif "/" in date:
        date = date.split("/")
    if len(date[0]) != 4:
        date = date[::-1]
    return "/".join(date)

def getSeason(unifiedDate: str) -> str:
    ymd = unifiedDate.split("/")
    year = int(ymd[0])
    month = int(ymd[1])
    if month >= 10:
        return str(year)+"/"+str(year+1)
    elif month <= 3:
        return str(year-1)+"/"+str(year)
    else:
        return "Off-Season"

teamNames = files.readFileToList("Data/teamNames.txt")
def getClosestTeamName(teamName: str) -> str:
    return sorted(teamNames, key=lambda savedName: jellyfish.jaro_similarity(savedName, teamName), reverse=True)[0]

playerNames = files.readFileToList("Data/playerNames.txt")
def getClosestPlayerName(playerName: str) -> str:
    closest = sorted(playerNames, key=lambda savedName: jellyfish.levenshtein_distance(savedName, playerName))[0]
    similarity = jellyfish.jaro_similarity(closest, playerName)
    if similarity > 0.7:
        return closest
    return "No Match"

goodShits = ["PointsTotal", "PointsDelta", "ServeTotal", "ServeError", "ServePoints", "ReceptionTotal", "ReceptionError", "AttackTotal", "AttackError", "AttackBlocked", "AttackPoints", "BlockPoints"]
def getPlayersFromTeam(game, teamNumber):
    players = {}
    for playerNumber in range(1,15):
        scores = []
        for goodShit in goodShits:
            value = game["{}Player{}Team{}".format(goodShit, playerNumber, teamNumber)]
            if type(value) == str:
                value = 0
            scores.append(value)
        playerName = game["NamePlayer{}Team{}".format(playerNumber, teamNumber)]
        if playerName != "":
            players[playerName] = scores
    return players

print("Reading Games")
games = []
for gameCSVPath in files.getAllFileNamesIn("Data/CSVs/"):
    game = files.readGameCSV(gameCSVPath)
    games.append(game)

gamesOnly = pd.DataFrame([], columns = ["Date","GameID","Season","M/F","Team1","Team2","Score1","Score2",
                                        "Player1Team1",
                                        "Player2Team1",
                                        "Player3Team1",
                                        "Player4Team1",
                                        "Player5Team1",
                                        "Player6Team1",
                                        "Player7Team1",
                                        "Player8Team1",
                                        "Player9Team1",
                                        "Player10Team1",
                                        "Player11Team1",
                                        "Player12Team1",
                                        "Player13Team1",
                                        "Player14Team1"
                                        "Player1Team2",
                                        "Player2Team2",
                                        "Player3Team2",
                                        "Player4Team2",
                                        "Player5Team2",
                                        "Player6Team2",
                                        "Player7Team2",
                                        "Player8Team2",
                                        "Player9Team2",
                                        "Player10Team2",
                                        "Player11Team2",
                                        "Player12Team2",
                                        "Player13Team2",
                                        "Player14Team2"])

print("Getting GamesOnly")
for game in games:
    d = {}
    date = unifyDates(game["Date"])
    d["Date"] = date
    gameID = game["MatchNumber"]
    d["GameID"] = gameID
    season = getSeason(date)
    d["Season"] = season
    team1 = getClosestTeamName(game["NameTeam1"])
    team2 = getClosestTeamName(game["NameTeam2"])
    d["Team1"] = team1
    d["Team2"] = team2
    score1 = int(game["ScoreTeam1"])
    score2 = int(game["ScoreTeam2"])
    d["Score1"] = score1
    d["Score2"] = score2
    mf = "-"
    if "Män" in game["League"]:
        mf = "M"
    elif "Fra" in game["League"]:
        mf = "F"
    d["M/F"] = mf
    playersTeam1 = list(getPlayersFromTeam(game, 1).keys())
    playersTeam2 = list(getPlayersFromTeam(game, 2).keys())
    for i in range(1, 15):
        player = "-"
        if len(playersTeam1) > i:
            player = playersTeam1[i-1]
            player = getClosestPlayerName(player)
        d["Player{}Team1".format(i)] = player
    for i in range(1, 15):
        player = "-"
        if len(playersTeam2) >= i:
            player = playersTeam2[i-1]
            player = getClosestPlayerName(player)
        d["Player{}Team2".format(i)] = player
        
    gamesOnly = gamesOnly.append(d, ignore_index=True)

print("Getting PlayerStats")

playerStatsPerGame = pd.DataFrame([], columns = ["PlayerName","M/F","PlayerTeam","OpposingTeam","Score1","Score2","Date","GameID","Season","PointsTotal", "PointsDelta", "ServeTotal", "ServeError", "ServePoints", "ReceptionTotal", "ReceptionError", "AttackTotal", "AttackError", "AttackBlocked", "AttackPoints", "BlockPoints"])

for game in games:
    date = unifyDates(game["Date"])
    gameID = game["MatchNumber"]
    season = getSeason(date)
    team1 = getClosestTeamName(game["NameTeam1"])
    team2 = getClosestTeamName(game["NameTeam2"])
    score1 = int(game["ScoreTeam1"])
    score2 = int(game["ScoreTeam2"])
    mf = "-"
    if "Män" in game["League"]:
        mf = "M"
    elif "Fra" in game["League"]:
        mf = "F"
    playersTeam1 = getPlayersFromTeam(game, 1)
    playersTeam2 = getPlayersFromTeam(game, 2)
    for playerName, stats in playersTeam1.items():
        playerName = getClosestPlayerName(playerName)
        row = {"PlayerName":playerName,
               "M/F":mf,
               "PlayerTeam":team1,
               "OpposingTeam":team2,
               "Score1":score1,
               "Score2":score2,
               "Date":date,
               "GameID":gameID,
               "Season":season,
               "PointsTotal":stats[0],
               "PointsDelta":stats[1],
               "ServeTotal":stats[2],
               "ServeError":stats[3],
               "ServePoints":stats[4],
               "ReceptionTotal":stats[5],
               "ReceptionError":stats[6],
               "AttackTotal":stats[7],
               "AttackError":stats[8],
               "AttackBlocked":stats[9],
               "AttackPoints":stats[10],
                "BlockPoints":stats[11]}
        playerStatsPerGame = playerStatsPerGame.append(row, ignore_index=True)
        
    for playerName, stats in playersTeam2.items():
        playerName = getClosestPlayerName(playerName)
        row = {"PlayerName":playerName,
               "M/F":mf,
               "PlayerTeam":team2,
               "OpposingTeam":team1,
               "Score1":score2,
               "Score2":score1,
               "Date":date,
               "GameID":gameID,
               "Season":season,
               "PointsTotal":stats[0],
               "PointsDelta":stats[1],
               "ServeTotal":stats[2],
               "ServeError":stats[3],
               "ServePoints":stats[4],
               "ReceptionTotal":stats[5],
               "ReceptionError":stats[6],
               "AttackTotal":stats[7],
               "AttackError":stats[8],
               "AttackBlocked":stats[9],
               "AttackPoints":stats[10],
                "BlockPoints":stats[11]}
        playerStatsPerGame = playerStatsPerGame.append(row, ignore_index=True)

gamesOnly.to_csv("GamesOnly.csv")
playerStatsPerGame.to_csv("PlayerStatsPerGame.csv")
        