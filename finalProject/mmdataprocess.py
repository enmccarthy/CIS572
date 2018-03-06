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
from rnn import getdataPoints

filename = "./DataFiles/RegularSeasonDetailedResults.csv"
# READ IN CSV DATA
df = pd.read_csv(filename, encoding="latin-1", low_memory=False)

# GENERATE SEASON+TEAM AVERAGES
all_col = ['Season', 'DayNum', 'WTeamID', 'WScore', 'LTeamID', 'LScore', 'WLoc',
       'NumOT', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR',
       'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3',
       'LFTM', 'LFTA', 'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']
winner_col = ['Season', 'WTeamID', 'WScore', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF']
loser_col = ['Season','LTeamID', 'LScore', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']
gen_col = ['Season','TeamID', 'Score', 'FGM', 'FGA', 'FGM3', 'FGA3', 'FTM', 'FTA', 'OR', 'DR', 'Ast', 'TO', 'Stl', 'Blk', 'PF', "ScoredON"]

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

grouped = wl_df.groupby(["Season", "TeamID"], as_index = False)
avg_stats = grouped.mean()
avg_stats = pd.DataFrame(avg_stats) # convert back into a dataframe
print(avg_stats.head())

# GENERATE TRAINING DATA from GAME data

print(getdataPoints(avg_stats, df))


