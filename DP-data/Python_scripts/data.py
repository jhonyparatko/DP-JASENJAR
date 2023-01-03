from importlib.resources import path
from xmlrpc.client import ResponseError
import pandas as pd
import time
from pytrends.request import TrendReq
import country_converter as coco

p = 'D:\DP-data\Google_Trans\\' #change D:\DP-data\ to your path

term = ['cat','dog', 'IVF', 'infertility'] #list of topics

r = 0
pytrends = TrendReq(hl='en-US', tz=0)

pytrends.build_payload(['petulka']) 
data=pytrends.interest_by_region()
reg = list(data.index.values) #getting list of all countries

region = coco.convert(names=reg, to='ISO2')
print (len(region))
time.sleep(3)

def get(term,region): 
    #getting results for term and country for years 2004-2020
    df = pd.DataFrame(columns=['Country','year',term])
    try:
        pytrends.build_payload([term],timeframe='all',geo=region)

        df = pytrends.interest_over_time()
    except ResponseError:
        time.sleep(300)
        df = get(term,region)
        
    if df.empty:
        return df
    val = df[term].to_list()
    dt = pd.DataFrame(columns=['Country','year',term])
    for i in range(1,18):
        #merging month values as mean year value
        x = 0
        for j in range(1,13):
            x += int(val[i*j-1])
        it = 2003 + i
        x=x/12
        dt = pd.concat([dt,pd.DataFrame({'Country':[reg[r]],'year':[it],term:[x]})],ignore_index=True)
    return dt

for i in term: 
    #cycle thru all terms
    r = 0 #if error 429 is rises just change r value to corresponded to last partial file number
    d = pd.DataFrame(columns=['Country','year',i])
    for j in range(r,len(region)):
        #cycle thru all country
        d2 = get(i,region[j])
        r += 1
        print (r)
        time.sleep(1)
        if r % 10 == 0:
            #save partial resurlts (when google trans is overloaded send error 429 and it fails even through sleep is used)
            pth = p  + i + str(r/10) + '.csv'
            d.to_csv(pth)
            time.sleep(300)
        if d2.empty:
            continue
        d = pd.concat([d,d2], ignore_index=True)
        