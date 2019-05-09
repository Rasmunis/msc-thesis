import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
from alarmType import getType
from alarmLocation import getLocation




#df_alarms_typeloc = pd.read_pickle('./pickles/df_alarms_typeloc')

#df_alarms_type_66 = df_alarms_typeloc[df_alarms_typeloc['Date'] == '2017-12-27']

#sns.set(style='darkgrid')

#ax = sns.countplot(x='Location', data=df_alarms_type_66)

#df_alarms_type_66['Location'].value_counts()[:10].plot(kind="bar")

df_alarms_typeloc = pd.read_pickle('./pickles/df_alarms_typeloc')

sns.set(style='darkgrid')

#df_alarms_type['Type'].value_counts()[:25].plot(kind="bar")

#print(df_alarms_type['Type'][df_alarms_type['Date'] == '2017-12-28'].value_counts())
"""
    Count alarmtype by time, template.
    countAlarms = df_alarms_typeloc[df_alarms_typeloc['Date_Time'] < datetime(2018, 1, 3)].resample('D', on='Date_Time').agg(lambda x: len(x[x['Type'] == 'DISTUT']))
"""

#countAlarms = df_alarms_typeloc[df_alarms_typeloc['Date_Time'] < datetime(2018, 7, 24)].resample('D', on='Date_Time').agg(lambda x: len(x[x['Type'] == 'DIFFUT']))

print(df_alarms_typeloc[df_alarms_typeloc['Type'].str.contains('OVERS')]['Type'])
print(df_alarms_typeloc.loc[55578])

#ax = countAlarms.plot()
#plt.show()