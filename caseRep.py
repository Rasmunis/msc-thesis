import pickle
from sklearn.metrics import jaccard_similarity_score
import numpy as np
from scipy.spatial.distance import euclidean

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
    'OVERSPÅ', 'OVERSST', 'OVERSNO', 'DISTUT', 'DISTAV', 'DISTPÅ', 'DISTST', 'DISTNO', 'OTHER'
]

def jaccardSimilarity(c1, c2):
    return jaccard_similarity_score(np.array([alarmTypeBinary(c1, alarmTypes)]), np.array([alarmTypeBinary(c2, alarmTypes)]))

def euclidianDist(c1, c2):
    return np.linalg.norm(np.array(alarmTypeProportion(c1, alarmTypes)) - np.array(alarmTypeProportion(c2, alarmTypes)))


def editDist(c1, c2):
    w = {
        'JORD': 1/49,
        'JORDVARIG': 1/5,
        'DISTPÅ': 1/22,
        'STRHIHI': 1,
        'DIFFST': 1/2,
        'DISTNO': 1/21,
        'DIFFUT': 1/2,
        'DIFFNO': 1/2,
        'OMFORMER': 1,
        'MOTORSPENNING': 1/2,
        'BRTUTE': 1/3,
        'OVERV': 1,
        'SSK': 1/2
    }
    m = len(c1) + 1
    n = len(c2) + 1
    r = np.zeros((m, n))
    k = np.zeros((m, n))

    for i in range(1, m):
        r[i][0] = r[i-1][0] + w[c1[i-1][0]]
    for j in range(1, n):
        r[0][j] = r[0][j-1] + w[c2[j-1][0]]
    for i in range(1, m):
        e = c1[i-1][0]
        for j in range(1, n):
            f = c2[j-1][0]
            if e == f:
                k[i][j] = 1/100 * abs(c1[i-1][1] - c2[j-1][1])
            else:
                k[i][j] = w[e] + w[f]

            r[i][j] = min([r[i-1, j] + w[e],
                           r[i, j-1] + w[f],
                           r[i-1, j-1] + k[i][j]
                           ])
    return r[-1][-1]

with open('./pickles/caseBase', 'rb') as cb:
    caseBase = pickle.load(cb)


with open('./pickles/v2/highFreqCases_v2', 'rb') as hfc:
    highFreqCases = pickle.load(hfc)

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
print(len(highFreqCases))
print(caseBase)

case0612 = [['JORD', 0],['JORD', 0],['JORD', 4],['JORD', 4],['JORD', 4],['JORD', 4],
                 ['JORD', 11],['JORD', 12],['JORD', 12],['JORD', 13],['JORD', 13],['JORD', 14],
                 ['JORD', 47],['JORD', 47],['DISTPÅ', 55],['DISTPÅ', 55],['DISTPÅ', 55],
                 ['DISTPÅ', 55],['DISTPÅ', 55],['DISTPÅ', 55],['JORDVARIG', 84],['JORDVARIG', 84],['JORDVARIG', 84],
                 ['STRHIHI', 168],['JORDVARIG', 222],['JORDVARIG', 242],['JORD', 384],['JORD', 384],
                 ['JORD', 599],['JORD', 599],['JORD', 602],['JORD', 602]]

case2812 = [['JORD', 0],['JORD', 0],['JORD', 0],['JORD', 0],['JORD', 0],['BRTUTE', 0],
            ['JORD', 0],['JORD', 0],['JORD', 0],['DIFFST', 0],['DIFFUT', 0],['DIFFST', 0],
            ['OVERV', 0],['BRTUTE', 0],['SSK', 0],['SSK', 0],['DIFFUT', 0],['JORD', 0],
            ['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],
            ['OMFORMER', 0], ['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],
            ['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0], ['DISTNO', 0],
            ['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],
            ['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],
            ['DISTNO', 0],['DISTNO', 0],['JORD', 0],['JORD', 0],['JORD', 0],['DISTNO', 0],
            ['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],['DISTNO', 0],['JORD', 0],
            ['BRTUTE', 0],['JORD', 0],['BRTUTE', 0],['DIFFNO', 0],['DIFFNO', 0],['JORD', 1],
            ['MOTORSPENNING', 1],['MOTORSPENNING', 1],['JORD', 1],['JORD', 3],['JORD', 3],
            ['JORD', 3],['JORD', 4],['JORD', 4],['JORD', 4],['JORD', 4],['JORD', 4],['JORD', 4],
            ['JORD', 4],['JORD', 4],['JORD', 4],['JORD', 4]]

case0111 = [['JORD', 0],['JORD', 0],['JORD', 0],['JORD', 0],['JORD', 0],['JORD', 0],
                 ['JORD', 0],['JORD', 0],['JORD', 0],['JORD', 0],['JORD', 0],['JORD', 0],
                 ['JORD', 0],['JORD', 0],['JORD', 0],['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],
                 ['DISTPÅ', 0],['DISTPÅ', 0],['DISTPÅ', 0],['JORDVARIG', 0],['JORDVARIG', 0],['JORDVARIG', 0],
                 ['JORDVARIG', 2],['JORD', 4],['JORD', 5], ['JORD', 5],['JORD', 5],['JORD', 7],['JORD', 7]]

caseEx1 = [['STRHIHI', 0], ['SSK', 75]]
caseEx2 = [['SSK', 0], ['SSK', 0]]

editDist(caseEx1, caseEx2)