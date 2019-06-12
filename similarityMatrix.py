import matplotlib.pyplot as plt
import pickle
import pandas as pd
import numpy as np
from caseRep import editDist, euclidianDist, jaccardSimilarity, alarmTypes

def similarityMatrix(floodSet1, floodSet2, simMeasure):
    simMatrix = []

    for f1 in floodSet1:
        row = []
        for f2 in floodSet2:
            row.append(simMeasure(f1, f2))
        simMatrix.append(row)
    return simMatrix

def matrixPlotter(simMatrix):
    fig, ax = plt.subplots()
    ax.matshow(simMatrix, cmap=plt.cm.Blues)
    plt.show()


with open('pickles/caseBase', 'rb') as cb:
    caseBase = pickle.load(cb)


with open('pickles/highFreqCases', 'rb') as hfc:
    alarmFloods = pickle.load(hfc)

alarmFloods = alarmFloods[:10] + alarmFloods[45:]

"""
print("Maintenenace start", alarmFloods[69], "\n\n\n")
print("Maintenance mid", alarmFloods[71], "\n\n\n")
print("Maintenance stop", alarmFloods[75], "\n\n\n")
"""

maintenanceTimestamps = [
    ('2018-07-26 10:18:00', '2018-08-08 14:30:00'),
    ('2018-10-10 23:35:00', '2018-10-11 07:25:00'),
    ('2018-02-15 13:49:00', '2018-02-15 13:58:00'),
    ('2017-01-10 11:37:00', '2017-01-10 12:37:00'),
    ('2018-03-21 11:22:00', '2018-04-23 15:32:00')
]

caseWeights = [
    {'important': [[pd.Timestamp('2018-11-08 18:26:35.110000'), 'BRTUTE', 'KLÆBU'], [pd.Timestamp('2018-11-08 18:26:36.270000'), 'BRTUTE', 'OSLOVEIE']]}
]

""" PRINT ALARMS THAT HAVE OTHER-TYPE
for i, case in enumerate(caseBase):
    for j, alarm in enumerate(case):
        if alarm[1] == "OTHER":
            print(alarm)
    print("\n\n\n")
"""


simMatrix = similarityMatrix(caseBase, alarmFloods, editDist)
matrixPlotter(simMatrix)