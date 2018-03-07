# Read and process March Madness data for consumption by SciKit-Learn

'''
NOTES:
   Most useful categories from adeshpande's model: (in order most to least)
   wins
   strength of schedule
   location
   SRS simple rating system (??)
   SPG average steals per game
   APG average assists per game
   TOP average turnovers per game
   RPG average rebounds per game
   3PG average 3's per game
   Tourney appearances
   PPG points per game scored
   PPGA points per game allowed
   Powerconf
   
  
KAGGLE COLUMNS - detailed results file
Season, DayNum, WTeamID, WScore, LTeamID, LScore, WLoc, and NumOT
WFGM - field goals made (by the winning team)
WFGA - field goals attempted (by the winning team)
WFGM3 - three pointers made (by the winning team)
WFGA3 - three pointers attempted (by the winning team)
WFTM - free throws made (by the winning team)
WFTA - free throws attempted (by the winning team)
WOR - offensive rebounds (pulled by the winning team)
WDR - defensive rebounds (pulled by the winning team)
WAst - assists (by the winning team)
WTO - turnovers committed (by the winning team)
WStl - steals (accomplished by the winning team)
WBlk - blocks (accomplished by the winning team)
WPF - personal fouls committed (by the winning team) 

additional features?
- total average score per game
- total average score ALLOWED

'''
import numpy as np
import pandas as pd
import random

filename = "./DataFiles/RegularSeasonDetailedResults.csv"
# READ IN CSV DATA
df = pd.read_csv(filename, encoding="latin-1", low_memory=False)

# GENERATE SEASON+TEAM AVERAGES
all_col = ['Season', 'DayNum', 'WTeamID', 'WScore', 'LTeamID', 'LScore', 'WLoc',
       'NumOT', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR',
       'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3',
       'LFTM', 'LFTA', 'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']
winner_col = ['Season', 'DayNum', 'WTeamID', 'WScore', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF']
loser_col = ['Season','DayNum', 'LTeamID', 'LScore', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']
gen_col = ['Season', 'DayNum', 'TeamID', 'Score', 'FGM', 'FGA', 'FGM3', 'FGA3', 'FTM', 'FTA', 'OR', 'DR', 'Ast', 'TO', 'Stl', 'Blk', 'PF', "ScoredON"]
wdf = df[winner_col]
ldf = df[loser_col]

# append Lscore to wdf, and Wscore to ldf
wdf = pd.concat([wdf, df["LScore"]], axis=1)
ldf = pd.concat([ldf, df["WScore"]], axis=1)
# assign identical column names to each dataframe
wdf.columns = gen_col 
ldf.columns = gen_col 
# vertically concatenate
wl_df = pd.concat([wdf,ldf], axis=0, ignore_index=True)

#print(wl_df.head())
#print(wl_df.to_string())
grouped = wl_df.groupby(["Season", "TeamID"], as_index = False).drop(['DayNum'])expanding().mean(axis=2).reset_index(0,drop=True)
groupAvg = pd.DataFrame(grouped)
groupAvg = groupAv
print(groupAvg[(groupAvg.TeamID == 1104)])
#avg_stats = grouped.expanding.mean()
#avg_stats = pd.DataFrame(avg_stats) # convert back into a dataframe
#print(avg_stats.head())

def createTablePerSeason(allData, teamID, season, currDay):
    newTable = allData[(allData.LTeamID == teamID) | (allData.WTeamID == teamID)]
    return newTable[(newTable.Season == season)]

def createTablePerDay(data, day):
    return data[data.DayNum <= day]


def getdataPoints(avgTable, allData):
    dataPoints = []
    #print(avgTable.to_string())
    for entry in allData.itertuples(index=False, name=None):
        season = entry[0]
        dayPlayed = entry[1]
        wT = entry[2]
        wScore = entry[3]
        lT = entry[4]
        lScore = entry[5]
        wAvg = avgTable[(avgTable.Season == season) & (avgTable.TeamID == wT) & (avgTable.DayNum == dayPlayed)]
        lAvg = avgTable[(avgTable.Season == season) & (avgTable.TeamID == lT) & (avgTable.DayNum == dayPlayed)]
        num = random.randrange(0, 100)/100.00
        if num <= .50:
            ans = lAvg.values-wAvg.values
            print("HERE")
            print(ans)
            #lol janky
            dataPoints.append(([season, dayPlayed, lT]+ ans[0].tolist()[3:], lScore-wScore))
            
        else:
            ans = wAvg.values-lAvg.values
            print("HERE")
            print(ans)
            dataPoints.append(([season, dayPlayed, wT]+ ans[0].tolist()[3:], wScore-lScore))
    return dataPoints

# GENERATE TRAINING DATA from GAME data

print(getdataPoints(groupAvg, df))


# location = "./DataFiles/"

# teamFileName = "Teams.csv"
# teamDF = pd.read_csv(location + teamFileName)

# seasonResultsName = "RegularSeasonDetailedResults.csv"
# seasonsDF = pd.read_csv(location + seasonResultsName)

# tourneySeedsName = "NCAATourneySeeds.csv"
# tourneySeedsDF = pd.read_csv(location + tourneySeedsName)

#mergedDF = teamDF.merge(tourneySeedsDF, on="TeamID")
