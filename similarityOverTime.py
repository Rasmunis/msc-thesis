import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import pickle
import caseRep
from scipy import stats
import numpy as np


def similarityOverTime(alarmList, caseBase, simFunc, stepSize):
    timeAxis = []
    similarityScores = [[] for n in range(len(caseBase))]
    for i in range(0, len(alarmList), stepSize):
        if (i % 1000 == 0):
            print("ALARM NO.", i)
            print(alarmList[i][0], "\n")
        startTime = alarmList[i][0]
        timeAxis.append(startTime)
        for j in range(len(caseBase)):
            case = caseBase[j]
            currentCase = []
            timeDiff = case[-1][0] - case[0][0]
            step = 0
            while alarmList[i + step][0] - startTime <= timeDiff:
                currentAlarm = alarmList[i + step]
                currentCase.append(currentAlarm)
                step += 1
            
            simScore = simFunc(case, currentCase)
            similarityScores[j].append(simScore)
    return timeAxis, similarityScores


def plotter(x, yList, start, end):
    startI = next(i for i, v in enumerate(x) if v > pd.Timestamp(start))
    endI = next(i for i, v in enumerate(x) if v > pd.Timestamp(end))

    labels = ['08-11-2018', '28-12-2017', '06-12-2017', '01-06-2016', '27-05-2016']
    #x = [n.time() for n in x]
    fig, ax = plt.subplots()

    for i, y in enumerate(yList):
        ax.plot(x[startI:endI], y[startI:endI], label=labels[i])
    plt.legend()
    fig.autofmt_xdate()
    plt.show()


"""  PRODUCING SIMILARITY DATA
with open('./pickles/caseBase', 'rb') as cb:
    caseBase = pickle.load(cb)

with open('./pickles/alarms_combined_case_format', 'rb') as accf:
    alarms_case_format = pickle.load(accf)

timeAxis, similarityScores = similarityOverTime(alarms_case_format, caseBase, caseRep.euclidianDist, 5)

with open('./pickles/FOLDERNAMEHERE/similarityScores', 'wb') as ss:
    pickle.dump(similarityScores, ss)

with open('./pickles/FOLDERNAMEHERE/timeAxis', 'wb') as ta:
    pickle.dump(timeAxis, ta)
"""


""" PLOTTING SIMILARITY DATA
with open('./pickles/FOLDERNAMEHERE/similarityScores', 'rb') as ss:
    ss = pickle.load(ss)
with open('./pickles/FOLDERNAMEHERE/timeAxis', 'rb') as ta:
    ta = pickle.load(ta)

plotter(ta, ss, start="2018-10-30", end="2018-11-30")
"""

""" SIMILARITY COMPARISON OF CASES IN CASEBASE
with open('./pickles/caseBase', 'rb') as cb:
    caseBase = pickle.load(cb)

for c1 in caseBase:
    for c2 in caseBase:
        print(c1[0][0].date(), " --- ", c2[0][0].date(), " == ", caseRep.editDist(c1, c2), "\n")
    print("\n\n\n")
"""

""" NORMALIZING EDIT DISTANCE
for i in range(len(ss)):
    avg = sum(ss[i])/len(ss[i])
    for j in range(len(ss[i])):
        ss[i][j] = ss[i][j]/avg
"""

""" CHECKING MATCHES FOR A CERTAIN SIM-VALUE
for i in range(len(ss[-1])):
    if ss[-1][i] < 0.25:
        print(ta[i])
"""

""" MAX MIN NORMALIZE SIMILARITY SCORES
for i in range(len(ss)):
    minSS = min(ss[i])
    maxSS = max(ss[i])
    for j, s in enumerate(ss[i]):
        ss[i][j] = ( ss[i][j] - minSS ) / ( maxSS - minSS )
"""

""" Z SCORE SS
for i in range(len(ss)):
    mean = np.mean(ss[i])
    std = np.std(ss[i])
    ss[i] = (ss[i] - mean) / std
"""


with open('./pickles/jaccardOverTimeData/similarityScores', 'rb') as ss:
    ss = pickle.load(ss)
with open('./pickles/jaccardOverTimeData/timeAxis', 'rb') as ta:
    ta = pickle.load(ta)

plotter(ta, ss, start="2016-05-26", end="2016-06-03")