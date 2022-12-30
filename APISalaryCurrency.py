import requests
import pandas as pd
@staticmethod
def get_currencies(filename):
    pd.set_option('expand_frame_repr', False)
    df = pd.read_csv(filename)
    sorted_currencies = df.groupby('salary_currency')['salary_currency'].count()
    sorted_currencies = sorted_currencies[sorted_currencies > 5000]
    print(sorted_currencies)
    dates = []
    sorted_currencies = sorted_currencies.to_dict()
    sorted_currencies = list(sorted_currencies.keys())
    sorted_currencies.remove('RUR')
    date_sort = df.sort_values(by='published_at')['published_at']
    start_year = int(date_sort.iloc[1].split('-')[0])
    start_month = int(date_sort.iloc[1].split('-')[1])
    end_year = int(date_sort.iloc[-1].split('-')[0])
    end_month = int(date_sort.iloc[-1].split('-')[1])
    results = pd.DataFrame(columns=['date'] + sorted_currencies)

    while start_year != end_year or start_month != end_month:
        if start_month in range(1, 10):
            dates.append('0{0}/{1}'.format(start_month, start_year))
        else:
            dates.append('{0}/{1}'.format(start_month, start_year))
        start_month += 1
        if start_month == 13:
            start_month = 1
            start_year += 1
    if start_month in range(1, 10):
        dates.append('0{0}/{1}'.format(start_month, start_year))
    else:
        dates.append('{0}/{1}'.format(start_month, start_year))
    print('Даты: ',dates)

    for i, j in enumerate(dates):
        url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{j}d=1'
        response = requests.get(url)
        curr = pd.read_xml(response.text)
        curr_sort = curr.loc[curr['CharCode'].isin(sorted_currencies + ['BYN'])]
        month_currencies = {}
        for currency in sorted_currencies:
            value = 0
            if currency == "RUR":
                continue
            if currency == 'BYR' or currency == 'BYN':
                value = float(
                    curr_sort.loc[curr_sort['CharCode'].isin(['BYR', 'BYN'])]['Value'].values[0].replace(',', '.')) / \
                        (curr_sort.loc[curr_sort['CharCode'].isin(['BYR', 'BYN'])]['Nominal'].values[0])
                month_currencies[currency] = value
            else:
                value = float(curr_sort.loc[curr_sort['CharCode'] == currency]['Value'].values[0].replace(',', '.')) / \
                        (curr_sort.loc[curr_sort['CharCode'] == currency]['Nominal'].values[0])
                month_currencies[currency] = value
        date = j.split('/')
        result = [f'{date[1]}-{date[0]}']
        for key, value in month_currencies.items():
            result.append(month_currencies[key])
        results.loc[i] = result

    results.to_csv('currencies.csv')
    print(results.head())

get_currencies('vacancies_dif_currencies.csv')