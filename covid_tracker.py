import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import json

new_cases = 'newCases'
cum_cases = 'cumCases'

payload = {
    'date': 'date',
    new_cases: 'newCasesBySpecimenDate',
    cum_cases: 'cumCasesBySpecimenDate',
}

lta_names = ['enfield', 'barnet', 'haringey']

for lta_name in lta_names:
    url = 'https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=utla;areaName={}&structure={}'.format(lta_name, json.dumps(payload))
    r = requests.get(url)
    x = r.json()
    data = x['data']
    json_data = []

    for d in data:
        y = {}
        date = datetime.datetime.strptime(d['date'],'%Y-%m-%d')
        y['date'] = date
        y['week'] = date.isocalendar()[1]
        y['newCases'] = int(d['newCases'])
        y['cumCases'] = int(d['cumCases'])
        y['ltaName'] = lta_name
        json_data.append(y)

    df = pd.DataFrame(json_data)
    df = df.sort_values(by='date', ascending=True)
    df['sma_7'] = df['newCases'].rolling(window=10).mean()
    df['ema'] = df['newCases'].ewm(span=10,adjust=False).mean()
    df.index = df.date
    df = df.tail(60)

    plt.figure(figsize=[15,10])
    plt.grid(True)
    
    x_pos = [i for i, _ in enumerate(df['date'])]
    plt.bar(df.index, df['newCases'], color='green')
    
    #plt.plot(df['newCases'],label='data')
    plt.plot(df['sma_7'],label='SMA 7 days')
    plt.plot(df['ema'],label='EMA')
    plt.xlabel("Date")
    plt.ylabel("New Cases")
    plt.title("{} New Cases per Day".format(lta_name))
    plt.legend(loc=2)
    plt.show()

    