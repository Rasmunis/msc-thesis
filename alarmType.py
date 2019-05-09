import pandas as pd

def getType(alarm):
    types = ['JORD', '::', 'SPENNREG', 'SPOLE', 'KJOLEVIFTER',
             'KORTSL', 'SAMB', 'LAV', '_JF', 'SSK', 'OMFORMER',
             'MOTORSPENNING', '_AC', 'BRANN', 'ENDESTILL',
             'SYNK', 'OVERV', 'SAMLEALARM', 'OVER', 'SPRINK', 'SIKR',
             'HJELPEKABEL', 'GASS', 'OLJE', 'UBALANSE', '_BR', 'PROT', 'TEMP', 'TRINNKOBLER', 'SOMMER']

    typeDict = {
        'JORD': 'JORD',
        '_JF': 'JORD',
    }

    unit = alarm['Unit']
    if unit == unit and unit is not None: # unit == unit is false if NaN
        unit = unit.strip()  # units have some case variations
        status = alarm['AT']
        if unit == 'kV' or unit == 'KV':
            return 'SPG' + status
        if unit == 'A':
            return 'STR' + status
        if unit == 'MVAr':
            return 'MVAR' + status

    value = alarm['Value']
    if value in ['UTE', 'INNE', 'MELLOM']:
        return 'BRT' + value

    tagname = alarm['Tagname']
    for ptype in ['DIFF', 'DIST', 'OVERS']:
        try:
            if ptype in tagname and value is not None:
                return ptype + value[:2]
        except:
            print("WAHAAT", ptype, " - - - ", value)

    desc = alarm['Description']
    for t in types:
        if t in alarm['Tagname']:
            if t in typeDict:
                return typeDict[t]
            else:
                return t
        if desc is not None:
            if '::' in desc:
                return 'HUMAN'

    return 'OTHER'

"""
df_alarms_filtered = pd.read_pickle('./pickles/df_alarms_filtered_combined')
df_alarms_filtered['Type'] = df_alarms_filtered.apply(lambda alarm: getType(alarm), axis=1)
df_alarms_filtered.to_pickle('./pickles/df_alarms_type_combined')
"""