import pickle
import pandas as pd
import gridGraph
import numpy as np
import matplotlib.pyplot as plt
from caseMaker import caseFormat

def locationCounter(case, stations, connections, maxSteps):
    countDict = {}

    for alarm in case:
        print(alarm)
        loc = alarm[2]
        comp = alarm[3]
        dir = alarm[4]
        countDict = updateCount(comp, dir, loc, countDict, stations, connections, 1, maxSteps)
    return countDict


def updateCount(comp, dir, loc, countDict, stations, connections, depth, maxSteps):
    if depth <= maxSteps:
        if comp is None and dir is None:
            countDict[loc] = countDict.get(loc, 0) + 1
            return countDict
        elif comp is not None and dir is None:
            if 1 in stations[loc][comp]:
                lineName = comp + '-' + "".join(connections[comp])
                countDict[lineName] = countDict.get(lineName, 0) + 1
            return countDict
        elif dir == 'BAKOVER':
            countDict[loc] = countDict.get(loc, 0) + 1
            for nextComp in stations[loc]:
                if nextComp != comp:
                    countDict = updateCount(nextComp, 'FOROVER', loc, countDict, stations, connections, depth + 1, maxSteps)
            return countDict
        elif dir == 'FOROVER':
            if 1 in stations[loc][comp]:
                for nextComp in connections[comp]:
                    lineName = comp + '-' + "".join(nextComp)
                    countDict[lineName] = countDict.get(lineName, 0) + 1
                    nextLoc = None
                    for stat, comps in stations.items():
                        if nextComp in comps:
                            nextLoc = stat
                            break
                    if nextLoc is None:
                        print("wtf is nextComp", nextComp)
                    countDict = updateCount(nextComp, 'BAKOVER', nextLoc, countDict, stations, connections, depth + 1, maxSteps)
                return countDict
            else:
                return countDict
        else:
            print("SOMETHING'S WRONG IN UPDATECOUNT", "\n", "comp = " + comp, "\n", "dir = " + dir, "\n", "loc = ", loc, "\n\n\n")
    else:
        return countDict



with open('./pickles/caseBase', 'rb') as cb:
    caseBase = pickle.load(cb)

with open('./pickles/df_alarms_cleaned', 'rb') as dfac:
    df_alarms_cleaned = pickle.load(dfac)

countDict = locationCounter(caseBase[4], gridGraph.stations, gridGraph.connections, 4)

#caseFollowUp = caseFormat(df_alarms_cleaned[(df_alarms_cleaned['Date_Time'] > caseBase[4][-1][0]) & (df_alarms_cleaned['Date_Time'] < pd.Timestamp('2016-06-01 20:24:00'))]) #FOLLOW

#countDictFollowing = locationCounter(caseFollowUp, gridGraph.stations, gridGraph.connections, 4) # FOLLOW

sorted_x = sorted(countDict.items(), key=lambda kv: kv[1])
#sorted_y = sorted(countDictFollowing.items(), key=lambda kv: kv[1]) #FOLLOW

#sorted_x = sorted_x + sorted_y #FOLLOW

for i in range(len(sorted_x)):
    setI = set(sorted_x[i][0].split('-'))
    for j in range(i+1, len(sorted_x)):
        setJ = set(sorted_x[j][0].split('-'))
        if setI == setJ:
            sorted_x[i] = (sorted_x[i][0], sorted_x[i][1] + sorted_x[j][1])
            sorted_x[j] = (sorted_x[j][0], 0)

sorted_x = sorted(sorted_x, key=lambda kv: kv[1])

objects = [x[0] for x in sorted_x]
y_pos = np.arange(len(objects))
performance = [x[1] for x in sorted_x]

plt.barh(y_pos[-10:], performance[-10:], align='center', alpha=0.5)
plt.yticks(y_pos[-10:], objects[-10:])
plt.gca().get_yticklabels()[-7].set_color("red")
plt.xlabel('No. Alarms')
plt.title('2016-05-27')

plt.show()
