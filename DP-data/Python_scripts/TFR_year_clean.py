import pandas as pd
from statistics import mean

df = pd.read_csv("D:\DP-data\\transform\TFR.csv", delimiter=';')

df.sort_values(by=['country', 'date'], inplace=True)
df_new = pd.DataFrame(columns=['country','date','value'])

country = df.country
country = set(country)
country = list(country)

for c in country:
    part = df[df.country == c]
    date = part.date
    date = set(date)
    date = list(date)
    for d in date:
        vals = part[part.date == d].value
        vals = list(vals)
        if len(vals) > 1:
            print (vals)
            vals = mean(vals)
            print (vals)
        else:
            vals = vals[0]
        df_new = pd.concat([df_new, pd.DataFrame({'country':[c],'date':[d],'value':[vals]})],ignore_index=True, axis = 0)
        

df_new.to_csv("D:\DP-data\\transform\TFR.csv", sep=';')

