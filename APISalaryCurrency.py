import pandas as pd
import requests
import lxml

pd.set_option("expand_frame_repr", False)

df = pd.read_csv("vacancies_dif_currencies.csv")
published_at_dates = df.loc[:, "published_at"]

oldest_record_publication_month = published_at_dates.min()[5:7]
latest_record_publication_month = published_at_dates.max()[5:7]

proper_currencies = [x for x in df
 .groupby("salary_currency")
 .size()
 .loc[lambda freq: freq >= 5000]
 .index
 .values if x != "RUR"]

result = pd.DataFrame(columns=["date"] + proper_currencies)

to_get_currencies_exchanges_dates = [
    f"{f'0{month}' if month in range(1, 9 + 1) else month}/{year}" for year in range(2003, 2022 + 1)
    for month in range(int(oldest_record_publication_month) if year == 2003 else 1,
                       int(latest_record_publication_month) if year == 2022 else 12 + 1)
]

if "BYR" in proper_currencies and "BYN" not in proper_currencies:
    proper_currencies.append("BYN")
elif "BYN" in proper_currencies:
    proper_currencies.append("BYR")


for i in range(len(to_get_currencies_exchanges_dates)):
    date = to_get_currencies_exchanges_dates[i]
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req=15/{date}d=1"
    response = requests.get(url)
    cur_df = pd.read_xml(response.text)
    cur_filtered_df = cur_df.loc[cur_df['CharCode'].isin(proper_currencies)]
    values = cur_filtered_df["Value"].apply(lambda x: float(x.replace(",", ".")))
    nominals = cur_filtered_df["Nominal"]
    exchanges = values / nominals
    result.loc[i] = [date.replace("/", "-")] + [x for x in exchanges]

result = result.set_index(result.loc[:, "date"])
result.to_csv("cb_currencies.csv", index=False)