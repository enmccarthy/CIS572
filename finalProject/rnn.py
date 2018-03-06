import pandas as pd
import numpy as np
import random
#read file
#take in entry for each game
location = "./DataFiles/"

teamFileName = "Teams.csv"
teamDF = pd.read_csv(location + teamFileName)

seasonResultsName = "RegularSeasonDetailedResults.csv"
seasonsDF = pd.read_csv(location + seasonResultsName)

tourneySeedsName = "NCAATourneySeeds.csv"
tourneySeedsDF = pd.read_csv(location + tourneySeedsName)


mergedDF = teamDF.merge(tourneySeedsDF, on="TeamID")

def createTablePerSeason(allData, teamID, season, currDay):
    newTable = allData[(allData.LTeamID == teamID) | (allData.WTeamID == teamID)]
    return newTable[(newTable.Season == season)]
    print(newTable.to_string())

def createTablePerDay(data, day):
    return data[data.DayNum <= day]


def getdataPoints(avgTable, allData):
    dataPoints = []
    #print(avgTable.to_string())
    for entry in allData.itertuples(index=False, name=None):
        season = entry[0]
        wT = entry[2]
        wScore = entry[3]
        lT = entry[4]
        lScore = entry[5]
        #I need to take off first two columns but I am lazy and havent yet
        wAvg = avgTable[(avgTable.Season == season) & (avgTable.TeamID == wT)]
        lAvg = avgTable[(avgTable.Season == season) & (avgTable.TeamID == lT)]
        num = random.randrange(0, 100)/100.00
        print(num)
        if num <= .50:
            print("HERE")
            print(lAvg)
            print(wAvg)
            print("HHHHHHHHHHEEEEEEEERRRRRRRRREEEEEEEEE")
            print(lAvg.values-wAvg.values)
            print(lAvg)
            lAvg = lAvg.subtract(wAvg, fill_value=0, axis=0)
            print("AFTER")
            print(lAvg)
            print(lAvg[lAvg.TeamID == lT].values.tolist())
            dataPoints.append((lAvg[lAvg.TeamID==lT].values.tolist(), lScore-wScore))
        else:
            print("OTHERHERE")
            wAvg.subtract(lAvg)
            print("OTHERAFTER")
            dataPoints.append((wAvg[wAvg.TeamID==wT].values.tolist(), wScore-lScore))
    return dataPoints
            
    
#getdataPoints(seasonsDF, seasonsDF)

