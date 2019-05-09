import pandas as pd
from filter import filterAlarm
from alarmType import getType, getDirection
from alarmLocation import getLocation, getComponent
import pickle
import gridGraph

"""
cols = ['Date', 'Time', 'Tagname', 'Description', 'Value', 'Unit', 'AT']

df_alarms = pd.read_csv('alarmer2016.csv', sep=';', names=cols, skiprows=4, engine='python', parse_dates=[['Date', 'Time']], dayfirst=True, keep_default_na=False)
df_alarms_end = pd.read_csv('365dagerEnd.csv', sep=';', names=cols, skiprows=2, engine='python', parse_dates=[['Date', 'Time']])


with open('./pickles/df_alarms_unmodified', 'rb') as df:
    df_alarms_end = pickle.load(df)

df_alarms_end = df_alarms_end[df_alarms_end['Date_Time'] >= pd.Timestamp('2017-01-01')]
df_alarms = df_alarms[df_alarms['Date_Time'] < df_alarms_end.iloc[0]['Date_Time']]
df_alarms_unmodified = pd.concat([df_alarms, df_alarms_end])

df_alarms_unmodified.to_pickle('./pickles/df_alarms_unmodified')
"""

with open('./pickles/df_alarms_unmodified', 'rb') as dau:
    df_alarms_unmodified = pickle.load(dau)

df_filtered = df_alarms_unmodified[df_alarms_unmodified.apply(lambda alarm: filterAlarm(alarm) == True, axis=1)]
df_filtered['Type'] = df_filtered.apply(lambda alarm: getType(alarm), axis=1)
df_filtered['Location'] = df_filtered.apply(lambda alarm: getLocation(alarm), axis=1)
df_filtered['Component'] = df_filtered.apply(lambda alarm: getComponent(alarm, gridGraph.stations), axis=1)
df_filtered['Direction'] = df_filtered.apply(lambda alarm: getDirection(alarm), axis=1)
df_filtered = df_filtered[df_filtered['Location'].notnull()]

#print(df_filtered[(df_filtered['Date_Time'] > pd.Timestamp('2017-12-28 05:01:00')) & (df_filtered['Date_Time'] < pd.Timestamp('2017-12-28 05:28:00'))])

df_filtered.to_pickle('./pickles/df_alarms_cleaned')

