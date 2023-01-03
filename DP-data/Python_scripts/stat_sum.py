from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

path = "C:\\Users\\jhonyparatko\\Desktop\\fact_table.csv"

df = pd.read_csv(path, delimiter=';')
df.sort_values(by=['name', 'lag', 'country'], inplace=True)

tmp = df['name']
na = set(tmp)
name = list(na)
tmp = df['lag']
la = set(tmp)
lag = list(la)


for n in name:
    corel = df[df.name == n]
    lg = 0
    clk = 0
    mx = 0
    mn = 0
    kl = 0
    cel = 0
    for l in lag:
        corelag = corel[corel.lag == l]
        tmp = corelag['country']
        co = set(tmp)
        country = list(co)
        celkem = 0
        true = 0
        max = 0
        min = 0
        klad = 0
        for c in country:
            sample = corelag[corelag.country == c]
            if len(sample) < 17:
                continue
            #print(sample.tfr)
            try:
                slope, intercept, r_value, p_value, std_err = stats.linregress(sample.tfr,sample.value)
            except ValueError:
                continue
            celkem += 1
            if p_value <= 0.05:
                true += 1
                if r_value > 0:
                    klad += 1
                    if max < r_value: 
                        max = r_value
                else:
                    if min > r_value:
                        min = r_value 
        if clk < true:
            clk, lg, mx, mn, kl, cel = true, l, max, min, klad, celkem
    print(n + " " + str(cel) + " " + str(clk) + " " + str(lg) + " " + str(kl) + " " + str(mx) + " " + str(mn))    
            




