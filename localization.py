import pickle
import pandas as pd
import gridGraph

def locationCounter(alarmList, stations, connections, maxSteps):
    countDict = {}

    for _, alarm in alarmList.iterrows():
        print(alarm)
        comp = alarm['Component']
        dir = alarm['Direction']
        loc = alarm['Location']
        countDict = updateCount(comp, dir, loc, countDict, stations, connections, 1, maxSteps)
    return countDict


def updateCount(comp, dir, loc, countDict, stations, connections, depth, maxSteps):
    if depth <= maxSteps:
        if comp is None and dir is None:
            countDict[loc] = countDict.get(loc, 0) + 1
            return countDict
        elif comp is not None and dir is None:
            lineName = comp + '-' + "".join(connections[comp])
            countDict[lineName] = countDict.get(lineName, 0) + 1
            return countDict
        elif dir == 'BAKOVER':
            countDict[loc] = countDict.get(loc, 0) + 1
            for nextComp in stations[loc]:
                return updateCount(nextComp, 'FOROVER', loc, countDict, stations, connections, depth + 1, maxSteps)
        elif dir == 'FOROVER':
            for nextComp in connections[comp]:
                lineName = comp + '-' + "".join(nextComp)
                countDict[lineName] = countDict.get(lineName, 0) + 1
                nextLoc = None
                for stat, comps in stations.items():
                    if nextComp in comps:
                        nextLoc = stat
                if nextLoc is None:
                    print("wtf is nextComp", nextComp)
                return updateCount(connections[comp], 'BAKOVER', nextLoc, countDict, stations, connections, depth + 1, maxSteps)
        else:
            print("SOMETHING'S WRONG IN UPDATECOUNT", "\n", "comp = " + comp, "\n", "dir = " + dir, "\n", "loc = ", loc, "\n\n\n")
    else:
        return countDict

with open('./pickles/df_alarms_cleaned', 'rb') as dac:
    df_alarms_cleaned = pickle.load(dac)

fault1206 = df_alarms_cleaned[(df_alarms_cleaned['Date_Time'] > pd.Timestamp('2016-06-01 20:11:33')) & (df_alarms_cleaned['Date_Time'] < pd.Timestamp('2016-06-01 20:11:41'))]

print(locationCounter(fault1206, gridGraph.stations, gridGraph.connections, 3))