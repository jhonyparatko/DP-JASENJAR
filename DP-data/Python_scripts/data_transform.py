from distutils.log import error
import country_converter as coco
import pandas as pd
import glob 
from importlib.resources import path
import random
from statsmodels.tsa.stattools import adfuller, kpss
import numpy as np

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            flat_list.append(element[1])
        else:
            flat_list.append(element)
    return flat_list

path = r'D:\DP-data\transform' # use your path for D:\DP-data\
endpath = 'D:\DP-data\Converted_Data_Sources'
all_files = glob.glob(path + "/*.csv")

print (all_files)

for file in all_files:
    df = pd.read_csv(file, delimiter=';')
    f = file.split('\\')
    print(f)
     
    country = coco.convert(names=df['country'], to='name_short')
    country = flatten_list(country)
    df['country'] = country
    
    country = set(country)
    country = list(country)
    try:
        country.remove('not found')
    except(ValueError):
        print("None")
    df = df[df.country != 'not found']
    df.sort_values(by=['country', 'date'], inplace=True)
    e = 0
    x = df.value
    x = list(x)
    try:
        for i in range(len(x)): 
            x[i] = x[i].replace(",", ".")
            x[i] = float(x[i])
            #print (x)
            df.value = x
    except(AttributeError):
        print (f[3])
    
    for c in random.choices(country, k=10):
        d = df[df.country == c]
        x = d.value
        
        try:
            result1 = adfuller(x)
            result2 = kpss(x)
        except(ValueError):
            e += 1
            continue
        
        if 0.05 < result1[1] and 0.05 > result2[1]:
            print ('ADF p-value: ' + str(result1[1]) + "\nKPSS p_value: " + str(result2[1]))
            e += 1
                    
    if e > 3:
        res_df = pd.DataFrame(columns=['country','date','value'])
        
        for c in country:
            d = df[df.country == c]
            d.sort_values(by=['date'], inplace=True)
            val = d.value
            val = np.array(val)
            val = np.diff(val)
            #print (val)
            val = val.tolist()
            val.insert(0, 0)
            for i in range(len(val)): val[i] = '{:.5f}'.format(val[i])
            d.value = val
            res_df = pd.concat([res_df,d],ignore_index=True)
        
        res_df.to_csv(endpath + '\\' + f[3])
    else:
        df.to_csv(endpath + '\\' + f[3])
    #creating of converted file

df = pd.read_csv(path + '\C\country.csv', delimiter=';')
country = coco.convert(names=df['country'], to='name_short')
df['country'] = country
df = df[df.country != 'not found']
df.to_csv(endpath + '\\' + 'country.csv')

