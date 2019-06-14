import pickle
from sklearn.metrics import jaccard_similarity_score
import numpy as np
from scipy.spatial.distance import euclidean
import pandas as pd
from math import sqrt

def alarmTypeBinary(alarmSet, alarmTypes):
    binaries = [0]*len(alarmTypes)
    for alarm in alarmSet:
        type = alarm[1]
        binaries[alarmTypes.index(type) if type in alarmTypes else -1] = 1
    return binaries

def alarmTypeProportion(alarmSet, alarmTypes):
    proportions = [0] * len(alarmTypes)
    for alarm in alarmSet:
        type = alarm[1]
        proportions[alarmTypes.index(type) if type in alarmTypes else -1] += 1
    proportions[:] = [p / len(alarmSet) for p in proportions]
    return proportions

alarmTypes = [
    'HUMAN', 'JORD', 'DIFFUT', 'DIFFAV', 'DIFFPÅ', 'DIFFST', 'DIFFNO', 'SPGHI', 'SPGHIHI', 'SPGLO',
    'SPGLOLO', 'SPGOK', 'STRHI', 'STRHIHI', 'STRLO', 'STRLOLO', 'STROK', 'MVARHI', 'MVARHIHI',
    'MVARLO', 'MVARLOLO', 'MVAROK', 'BRTUTE', 'BRTINNE', 'BRTMELLOM', 'OVERSUT', 'OVERSAV',
    'OVERSPÅ', 'OVERSST', 'OVERSNO', 'DISTUT', 'DISTAV', 'DISTPÅ', 'DISTST', 'DISTNO',
    'OVERV', 'SSK', 'LAV', 'DIFFVA', 'OMFORMER', 'SIKR', 'MOTORSPENNING', 'SPENNTR',
    'AUTO/HAND', 'SKILLEBR', 'DISDIF', 'EFFBRY', 'LIKERETTER', 'NODLYS', 'OTHER'
]

def jaccardSimilarity(c1, c2):
    return jaccard_similarity_score(np.array([alarmTypeBinary(c1, alarmTypes)]), np.array([alarmTypeBinary(c2, alarmTypes)]))

def euclidianDist(c1, c2):
    return np.linalg.norm(np.array(alarmTypeProportion(c1, alarmTypes)) - np.array(alarmTypeProportion(c2, alarmTypes)))

def euclidianDistWeighted(c1, c2):
    c1prop = alarmTypeProportion(c1, alarmTypes)
    c2prop = alarmTypeProportion(c2, alarmTypes)
    important = ['BRTUTE', 'DIFFUT', 'DISTUT']
    sum = 0
    for i, type in enumerate(alarmTypes):
        if type in important:
            sum += (c1prop[i] - c2prop[i])**2*2
        else:
            sum += (c1prop[i] - c2prop[i])**2
    return sqrt(sum)

def editDist(c1, c2):
    w = {}

    for a in (c1):
        w[a[1]] = (w.get(a[1], 1)**-1 + 1)**-1
    

    m = len(c1) + 1
    n = len(c2) + 1
    r = np.zeros((m, n))
    k = np.zeros((m, n))

    for i in range(1, m):
        r[i][0] = r[i-1][0] + w.get(c1[i-1][1], 1)
    for j in range(1, n):
        r[0][j] = r[0][j-1] + w.get(c2[j-1][1], 1)
    for i in range(1, m):
        e = c1[i-1][1]
        for j in range(1, n):
            f = c2[j-1][1]
            if e == f:
                k[i][j] = 1/100 * abs((c1[i-1][0] - c2[j-1][0]).total_seconds()) # total_seconds converts the Timedelta into secs 
            else:
                k[i][j] = w.get(e, 1) + w.get(f, 1)

            r[i][j] = min([r[i-1, j] + w.get(e, 1),
                           r[i, j-1] + w.get(f, 1),
                           r[i-1, j-1] + k[i][j]
                           ])
    return r[-1][-1]/n


""" CASE BASE AND ALARMS WITH JACCARD
for newCase in highFreqCases:
    for oldCase in caseBase:
        similarity = jaccardSimilarity(newCase, oldCase)
        if similarity > 0.3:
            print("SCORE", similarity)
            print("NEWCASE", newCase)
            print("OLDCASE", oldCase)
            print('\n\n\n')
"""

""" CASE BASE AND ALARMS WITH EUCLIDIAN
for newCase in highFreqCases:
    for oldCase in caseBase:
        distance = euclidianDist(newCase, oldCase)
        if distance < 0.7:
            print("SCORE", distance)
            print("NEWCASE", newCase)
            print("OLDCASE", oldCase)
            print('\n\n\n')
"""


caseEx1 = [
    [pd.Timestamp('2017-12-28 05:24:43.820000'), 'JORD'], [pd.Timestamp('2017-12-28 05:24:43.820000'), 'JORD'],
    [pd.Timestamp('2017-12-28 05:24:43.820000'), 'DISTAV'], [pd.Timestamp('2017-12-28 05:24:43.820000'), 'DISTAV']]

caseEx2 = [
    [pd.Timestamp('2017-12-28 05:24:43.820000'), 'JORD'], [pd.Timestamp('2017-12-28 05:24:48.820000'), 'JORD'],
    [pd.Timestamp('2017-12-28 05:40:43.820000'), 'DISTPÅ'], [pd.Timestamp('2017-12-28 05:40:43.820000'), 'DISTPÅ']]

caseEx3 = []