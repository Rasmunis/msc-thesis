import matplotlib.pyplot as plt
import pickle
import pandas as pd
import numpy as np
from caseRep import editDist, euclidianDist, jaccardSimilarity, alarmTypes, euclidianDistWeighted
from scipy.stats import zscore

def similarityMatrix(floodSet1, floodSet2, simMeasure):
    simMatrix = []

    for f1 in floodSet1:
        row = []
        for f2 in floodSet2:
            row.append(simMeasure(f1, f2))
            
        simMatrix.append(row)
    return simMatrix

def matrixPlotter(simMatrix, showVals):
    fig, ax = plt.subplots()
    ax.matshow(simMatrix, cmap=plt.cm.Blues_r)
    if showVals:
        for i in range(len(simMatrix)):
            for j in range(len(simMatrix[0])):
                c = round(simMatrix[i][j], 3)
                ax.text(j, i, str(c), va='center', ha='center')
    plt.show()


with open('pickles/caseBase', 'rb') as cb:
    caseBase = pickle.load(cb)


with open('pickles/double_filtered_hfc', 'rb') as hfc:
    alarmFloods = pickle.load(hfc)

alarmFloods = alarmFloods[:10] + alarmFloods[44:]
alarmFloods = alarmFloods[:50] + alarmFloods[76:]
alarmFloods = alarmFloods[:18] + alarmFloods[36:]
alarmFloods = alarmFloods[:7] + alarmFloods[8:]

for case in caseBase[4]:
    print(case)
caseWeights = [
    {'important': [
        [pd.Timestamp('2018-11-08 18:26:35.110000'), 'BRTUTE', 'KLÆBU', 'H2', None],
        [pd.Timestamp('2018-11-08 18:26:36.270000'), 'BRTUTE', 'OSLOVEIE', 'OSA', None],
        [pd.Timestamp('2018-11-08 18:26:36.190000'), 'DISTUT', 'OSLOVEIE', 'OSA', None]
    ]},
    {'important': [
        [pd.Timestamp('2017-12-28 05:24:40.260000'), 'DIFFUT', 'FOSSEGRE', 'FS', None],
        [pd.Timestamp('2017-12-28 05:24:40.270000'), 'DIFFUT', 'STRINDA', 'FO1', None],
        [pd.Timestamp('2017-12-28 05:24:40.350000'), 'BRTUTE', 'STRINDA', 'FO1', None],
        [pd.Timestamp('2017-12-28 05:24:40.360000'), 'BRTUTE', 'FOSSEGRE', 'FS', None]
    ]},
    {'important': [
        [pd.Timestamp('2017-12-06 04:52:57.400000'), 'STRHIHI', 'PAULINELU', None, None]
    ]},
    {'important': [
        [pd.Timestamp('2016-06-01 20:12:02.230000'), 'DIFFUT', 'MOHOLT', 'MP2', None],
        [pd.Timestamp('2016-06-01 20:12:02.060000'), 'DIFFUT', 'PAULINELU', 'PM2', None],
        [pd.Timestamp('2016-06-01 20:12:02.320000'), 'BRTUTE', 'MOHOLT', 'MP2', None],
        [pd.Timestamp('2016-06-01 20:12:02.590000'), 'DISTUT', 'VESTBYEN', 'VT', None],
        [pd.Timestamp('2016-06-01 20:12:02.630000'), 'BRTUTE', 'VESTBYEN', 'VT', None],
        [pd.Timestamp('2016-06-01 20:12:02.860000'), 'DISTUT', 'STRINDA', 'M1', None],
        [pd.Timestamp('2016-06-01 20:12:02.880000'), 'DISTUT', 'STRINDA', 'M2', None],
        [pd.Timestamp('2016-06-01 20:12:02.890000'), 'BRTUTE', 'PAULINELU', 'PM1', None],
        [pd.Timestamp('2016-06-01 20:12:02.950000'), 'BRTUTE', 'STRINDA', 'M1', None],
        [pd.Timestamp('2016-06-01 20:12:02.970000'), 'BRTUTE', 'STRINDA', 'M2', None],
        [pd.Timestamp('2016-06-01 20:12:03.050000'), 'DIFFUT', 'MOHOLT', 'MP1', None],
        [pd.Timestamp('2016-06-01 20:12:03.150000'), 'BRTUTE', 'MOHOLT', 'MP1', None],
    ]},
    {'important': []}
]
print(len(caseBase[0]))
for i in range(len(caseBase)):
    for alarm in caseWeights[i]['important']:
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
        caseBase[i].insert(caseBase[i].index(alarm), alarm)
print(len(caseBase[0]))

alarmFloods[18] = caseBase[2]
alarmFloods[22] = caseBase[1]
alarmFloods[36] = caseBase[0]
alarmFloods[7] = caseBase[3]


print(alarmFloods[23])
print("\n\n\n", alarmFloods[24])
print("\n\n\n", alarmFloods[41])
print("\n\n\n", alarmFloods[20]) 
print("\n\n\n", alarmFloods[30])
print("\n\n\n", alarmFloods[35])
""" PRINT ALARMS THAT HAVE OTHER-TYPE
for i, case in enumerate(caseBase):
    for j, alarm in enumerate(case):
        if alarm[1] == "OTHER":
            print(alarm)
    print("\n\n\n")
"""
#simMatrix = similarityMatrix(alarmFloods, caseBase, euclidianDistWeighted)
"""
for i in range(len(simMatrix)):
    list = np.array(simMatrix[i])
    min = np.min(list)
    max = np.max(list)
    simMatrix[i] = zscore(simMatrix[i])"""
#matrixPlotter(simMatrix, False)