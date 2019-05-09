import pandas as pd
from matplotlib import pyplot as plt
import datetime

feil66 = pd.read_csv('feil66.csv', sep=';')

feil66 = feil66[feil66['Relevant'] == 1]

print(feil66.columns.values)

#feil66['klokken'] = feil66['klokken'].str.split('.', expand=True)[0]
feil66['klokken'] = feil66['klokken'].str.strip()
feil66['klokken'] = pd.to_datetime(feil66['klokken'], format='%H:%M:%S.%f').dt.time
feil66['plassering'] = feil66['melding 1'].str.split('_', expand=True)[0]

print(feil66['klokken'])

def showByLocation():
    countByLocation = feil66[['klokken', 'plassering']]

    countByLocation = countByLocation[countByLocation['plassering'].apply(lambda x: len(x.split(' '))) < 2]

    counts = pd.get_dummies(countByLocation['plassering']).cumsum()

    countByLocation = countByLocation.join(counts).groupby('klokken').agg(min)

    print(countByLocation['FOSSEGRE'])

    countByLocation = countByLocation.loc[datetime.time(hour=5, minute=10):datetime.time(hour=5, minute=25)]

    ax = countByLocation.plot(y=['BELL', 'BRUDAL', 'FLATÅSEN', 'FOSSEGRE', 'HUSEBY', 'MEL251',
     'MIDTBYEN', 'MOHOLT', 'PAULINELU', 'SOKNA', 'STORHAUGE', 'STRINDA', 'SUM', 'TEN',
     'TRONDHEIM', 'UNIVERSI', 'VESTBYEN', 'VI1'])

    ax.legend(loc="upper left", bbox_to_anchor=(0, 1.15), ncol=2, fancybox=True)
    plt.show()

showByLocation()