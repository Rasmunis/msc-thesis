import pandas as pd


def getLocation(alarm):
    locations = ['UNIVERSI', 'RANHEIM', 'BELBUAN', 'LADE', 'BRATSBERG', 'HESTTRØ', 'STRINDA',
                 'MOHOLT', 'MIDTBYEN', 'BURAN', 'FOSSEGRE', 'PAULINELU', 'VESTBYEN', 'ØLEIRFOSS',
                 'OSLOVEIE', 'STAVNE', 'STORHAUGE', 'FLATÅSEN', 'HUSEBY', 'GAUSTAD', 'KLÆBU',
                 'FJÆREMSFO', 'TILLER']

    splitTag = alarm.get('Tagname').split('_')
    firstElem = splitTag[0]

    if firstElem != 'SUM':
        if firstElem in locations:
            return firstElem
    else:
        lastElem = splitTag[-1]
        if lastElem in locations:
            return splitTag[-1]
    return None

"""
df_alarms_type = pd.read_pickle('./pickles/df_alarms_type_v2')
df_alarms_type['Location'] = df_alarms_type.apply(lambda alarm: getLocation(alarm), axis=1)
df_alarms_type = df_alarms_type[df_alarms_type['Location'].notnull()]
df_alarms_type.to_pickle('./pickles/df_alarms_typeloc_v2')
"""