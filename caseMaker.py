import pandas as pd
from sklearn.metrics import jaccard_similarity_score
import numpy as np
import pickle

#df_alarms_typeloc = pd.read_pickle('./pickles/df_alarms_typeloc_v2')

#print(df_alarms_typeloc)

def caseMaker(df, timeDiff, sizeLimit):
    highFreqCases = []
    tempCase = []
    actualIndex = 0
    for index, row in df[:-1].iterrows():
        rowTime = row['Date_Time']
        rowType = row['Type']
        rowLoc = row['Location']

        tempCase.append([rowTime, rowType, rowLoc])
        if (df.iloc[actualIndex + 1]['Date_Time'] - rowTime) > pd.Timedelta(timeDiff):
            if len(tempCase) >= sizeLimit:
                highFreqCases.append(tempCase)
            tempCase = []
        actualIndex += 1
    return highFreqCases

def extractCase(startTime, endTime, alarmList):
    startI = next(i for i, v in enumerate(alarmList) if v[0] > pd.Timestamp(startTime))
    endI = next(i for i, v in enumerate(alarmList) if v[0] > pd.Timestamp(endTime))
    return alarmList[startI:endI]

def caseFormat(df):
    caseList = []
    for _, row in df.iterrows():
        rowTime = row['Date_Time']
        rowType = row['Type']
        rowLoc = row['Location']

        caseList.append([rowTime, rowType, rowLoc])
    return caseList

def printPretty(caseList):
    for case in caseList:
        print('')
        print('===============================')
        print('')
        for alarm in case:
            print(alarm)
        print('')
        print('===============================')
        print('')


""" REFORMAT ALARM LIST INTO CASE-FORMAT
with open('./pickles/df_alarms_cleaned', 'rb') as dac:
    df_alarms_cleaned = pickle.load(dac)

alarms_combined_case_format = caseFormat(df_alarms_cleaned)

with open('./pickles/alarms_combined_case_format', 'wb') as accf:
    pickle.dump(alarms_combined_case_format, accf)
"""

""" UPDATE CASE-BASE

caseTimestamps = [
    ('2018-11-08 18:26:33', '2018-11-08 18:26:39'),
    ('2017-12-28 05:24:39', '2017-12-28 05:24:45'),
    ('2017-12-06 04:52:55', '2017-12-06 04:53:02'),
    ('2016-06-01 20:11:33', '2016-06-01 20:12:11'),
    ('2016-05-27 21:36:35', '2016-05-27 21:36:49')
]

with open('./pickles/alarms_combined_case_format', 'rb') as hfc:
    alarmList = pickle.load(hfc)

with open('./pickles/caseBase', 'rb') as cb:
    caseBase = pickle.load(cb)

caseBase = []

for case in caseTimestamps:
    caseBase.append(extractCase(case[0], case[1], alarmList))

with open('./pickles/caseBase', 'wb') as cb:
    pickle.dump(caseBase, cb)
"""

""" Find and save alarm-floods
with open('./pickles/df_alarms_cleaned', 'rb') as dac:
    df_alarms_cleaned = pickle.load(dac)

with open('./pickles/alarms_combined_case_format', 'rb') as accf:
    alarms_combined_case_format = pickle.load(accf)

print(df_alarms_cleaned.iloc[7900])
print(alarms_combined_case_format[7900:7905])
highFreqCases = caseMaker(df_alarms_cleaned, '3s', 30)

with open('./pickles/highFreqCases', 'wb') as hfc:
    pickle.dump(highFreqCases, hfc)
"""


with open('./pickles/caseBase', 'rb') as cb:
    caseBase = pickle.load(cb)

for alarm in caseBase[-1]:
    print(alarm)
