import pandas as pd
from filter import filterAlarm
from alarmType import getType
from alarmLocation import getLocation
import pickle

cols = ['Date', 'Time', 'Tagname', 'Description', 'Value', 'Unit', 'AT']

dateCon = lambda x: pd.datetime.strptime(x, "%d.%m.%Y %H:%M:%S.%f")
timeCon = lambda x: pd.datetime.strptime(x, '%H:%M:%S.%f')

df_alarms = pd.read_csv('alarmer2016.csv', sep=';', names=cols, skiprows=4, engine='python', parse_dates=[['Date', 'Time']], dayfirst=True, keep_default_na=False)
print("2016 FORMAT HEAD", df_alarms[(df_alarms['Date_Time'] > pd.Timestamp("2016-06-01 17:11:00")) & (df_alarms['Date_Time'] < pd.Timestamp("2016-06-01 20:13:00"))].head(), "\n\n\n")
print("2016 INDEX AROUND 9600", df_alarms.iloc[9880], "\n\n\n")
#df_alarms_end = pd.read_csv('365dagerEnd.csv', sep=';', names=cols, skiprows=2, engine='python', parse_dates=[['Date', 'Time']])


with open('./pickles/df_alarms_unmodified', 'rb') as df:
    df_alarms_end = pickle.load(df)

print("DF_ALARMS_END PICKLE HEAD", df_alarms_end.head(), "\n\n\n")

df_alarms_end = df_alarms_end[df_alarms_end['Date_Time'] >= pd.Timestamp('2017-01-01')]
print("DF_ALARMS_END AFTER 2016", df_alarms_end.head(), "\n\n\n")
df_alarms = df_alarms[df_alarms['Date_Time'] < df_alarms_end.iloc[0]['Date_Time']]
print("2016 TAIL AFTER TIME STUFF", df_alarms[(df_alarms['Date_Time'] > pd.Timestamp("2016-06-01 17:11:00")) & (df_alarms['Date_Time'] < pd.Timestamp("2016-06-01 20:13:00"))].head())
df_alarms_unmodified = pd.concat([df_alarms, df_alarms_end])
print("CONCATED HEAD", df_alarms_unmodified[(df_alarms_unmodified['Date_Time'] > pd.Timestamp("2016-06-01 17:11:00")) & (df_alarms_unmodified['Date_Time'] < pd.Timestamp("2016-06-01 20:13:00"))].head(), "\n\n\n")

df_alarms_unmodified.to_pickle('./pickles/df_alarms_unmodified')

df_filtered = df_alarms_unmodified[df_alarms_unmodified.apply(lambda alarm: filterAlarm(alarm) == True, axis=1)]
print("FILTERED FIRST JUNE 2016", df_filtered[(df_filtered['Date_Time'] > pd.Timestamp("2016-06-01 17:11:00")) & (df_filtered['Date_Time'] < pd.Timestamp("2016-06-01 20:13:00"))].head())
df_filtered['Type'] = df_filtered.apply(lambda alarm: getType(alarm), axis=1)
print("FILTERED AFTER TYPE FIRST JUNE 2016", df_filtered[(df_filtered['Date_Time'] > pd.Timestamp("2016-06-01 17:11:00")) & (df_filtered['Date_Time'] < pd.Timestamp("2016-06-01 20:13:00"))].head())
df_filtered['Location'] = df_filtered.apply(lambda alarm: getLocation(alarm), axis=1)
print("FILTERED AFTER LOCATION FIRST JUNE 2016", df_filtered[(df_filtered['Date_Time'] > pd.Timestamp("2016-06-01 17:11:00")) & (df_filtered['Date_Time'] < pd.Timestamp("2016-06-01 20:13:00"))].head())
df_alarms_cleaned = df_filtered[df_filtered['Location'].notnull()]
print("ALARMS CLEANED AFTER NOT NULL JUNE 2016", df_alarms_cleaned[(df_alarms_cleaned['Date_Time'] > pd.Timestamp("2016-06-01 17:11:00")) & (df_alarms_cleaned['Date_Time'] < pd.Timestamp("2016-06-01 20:13:00"))].head())
df_alarms_cleaned.to_pickle('./pickles/df_alarms_cleaned')


with open('./pickles/df_alarms_cleaned', 'rb') as dac:
    df_alarms_cleaned = pickle.load(dac)

print(df_alarms_cleaned[(df_alarms_cleaned['Date_Time'] > pd.Timestamp("2016-06-01 17:11:00")) & (df_alarms_cleaned['Date_Time'] < pd.Timestamp("2016-06-01 20:13:00"))])