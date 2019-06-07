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

print("Maintenenace start", alarmFloods[113], "\n\n\n")
print("Maintenance stop", alarmFloods[128])

print("CASEBASE 1", caseBase[1])
print("JACCSIM C0 AND 113", jaccardSimilarity(caseBase[0], alarmFloods[113]), "\n\n")
print("JACCSIM C1 AND 113", jaccardSimilarity(caseBase[1], alarmFloods[113]), "\n\n")
print("JACCSIM C0 AND 128", jaccardSimilarity(caseBase[0], alarmFloods[128]), "\n\n")
print("JACCSIM C1 AND 128", jaccardSimilarity(caseBase[1], alarmFloods[128]), "\n\n")

for i in range(len(caseBase[3])):
    if caseBase[3][i][1] not in alarmTypes:
        print(caseBase[3][i][1])
#simMatrix = similarityMatrix(caseBase, alarmFloods, jaccardSimilarity)
#print(simMatrix)
#matrixPlotter(simMatrix)