import pandas as pd


def filterAlarm(alarm):
    noise = ['_SAMB', '_RTU', 'BELL', '_012', '_220V']
    tagname = alarm['Tagname']

    for n in noise:
        if n in tagname:
            return False

    return True

"""
df_alarms = pd.read_pickle('./pickles/df_alarms_combined')
df_alarms = df_alarms[df_alarms.apply(lambda alarm: filterAlarm(alarm) == True, axis=1)]
df_alarms.to_pickle('./pickles/df_alarms_filtered_combined')
"""