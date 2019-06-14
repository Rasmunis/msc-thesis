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
        rowComp = row['Component']
        rowDir = row['Direction']

        caseList.append([rowTime, rowType, rowLoc, rowComp, rowDir])
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

""" REMOVE MAINTENANCE ALARMS
with open('./pickles/alarms_combined_case_format', 'rb') as accf:
    alarms_combined_case_format = pickle.load(accf)

maintenanceTimestamps = [
    ('2018-06-15 00:00:00', '2018-06-22 23:59:00'),
    ('2018-07-26 10:18:00', '2018-08-08 14:30:00'),
    ('2018-10-10 23:35:00', '2018-10-11 07:25:00'),
    ('2018-02-15 13:49:00', '2018-02-15 13:58:00'),
    ('2017-01-10 11:37:00', '2017-01-10 12:37:00'),
    ('2018-03-21 11:22:00', '2018-04-23 15:32:00')
]

filtered_accf = []

for alarm in alarms_combined_case_format:
    is_maintenance = False
    for timeInterval in maintenanceTimestamps:
        start = pd.Timestamp(timeInterval[0])
        end = pd.Timestamp(timeInterval[1])
        if alarm[0] > start and alarm[0] < end:
            is_maintenance = True
    
    if not is_maintenance:
        filtered_accf.append(alarm)

with open('./pickles/filtered_accf', 'wb') as faccf:
    pickle.dump(filtered_accf, faccf)
"""

with open('./pickles/filtered_hfc', 'rb') as hfc:
    highFreqCases = pickle.load(hfc)

maintenanceTimestamps = [
    ('2018-06-15 00:00:00', '2018-06-22 23:59:00'),
    ('2018-07-26 10:18:00', '2018-08-08 14:30:00'),
    ('2018-10-10 23:35:00', '2018-10-11 07:25:00'),
    ('2018-02-15 13:49:00', '2018-02-15 13:58:00'),
    ('2017-01-10 11:37:00', '2017-01-10 12:37:00'),
    ('2018-03-21 11:22:00', '2018-04-23 15:32:00')
]

caseFollowUpTimestamps = [
    ('2018-11-08 18:26:39', '2018-11-08 23:59:00'),
    ('2017-12-28 05:24:45', '2017-12-28 23:59:00'),
    ('2017-12-06 04:53:02', '2017-12-06 23:59:00'),
    ('2016-06-01 20:12:11', '2016-06-01 23:59:00'),
    ('2016-05-27 21:36:49', '2016-05-27 23:59:00')
]

filtered_hfc = []
for case in highFreqCases:
    is_maintenance = False
    for alarm in case:
        for timeInterval in caseFollowUpTimestamps:
            start = pd.Timestamp(timeInterval[0])
            end = pd.Timestamp(timeInterval[1])
            if alarm[0] > start and alarm[0] < end:
                is_maintenance = True
        
    if not is_maintenance:
        filtered_hfc.append(case)

with open('./pickles/double_filtered_hfc', 'wb') as fhfc:
    pickle.dump(filtered_hfc, fhfc)