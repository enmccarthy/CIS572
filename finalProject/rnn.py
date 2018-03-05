import pandas as pd
import numpy as np
#read file
#take in entry for each game
location = "./DataFiles/"
teamFileName = "Teams.csv"
teamDF = pd.read_csv(location + teamFileName)
print(teamDF.to_string())

seasonResultsName = "RegularSeasonDetailedResults.csv"
seasonsDF = pd.read_csv(location + seasonResultsName)

tourneySeedsName = "NCAATourneySeeds.csv"
tourneySeedsDF = pd.read_csv(location + tourneySeedsName)

print(tourneySeedsDF.to_string())

mergedDF = teamDF.merge(tourneySeedsDF, on="TeamID")
print(mergedDF.to_string())