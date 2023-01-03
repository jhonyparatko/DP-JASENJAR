from pickle import TRUE
import country_converter as coco
import pandas as pd
from importlib.resources import path

ls = []
for i in range (1,26):
    ls.append(str(i))
terms = ['cat','dog', 'IVF', 'infertility']
pt = 'D:\DP-data\\'
#change path to yours
for term in terms:
    df = pd.DataFrame(columns=['Country','year',term])

    for i in ls:
        #merging files to one
        d = pd.read_csv(pt+'Google_Trans\\'+term+i+'.0.csv')
        df = pd.concat([df,d],ignore_index=True)
    
    df.drop_duplicates(inplace=True) #cleaning duplicates if exists
    country = coco.convert(names=df['Country'], to='name_short')
    df['Country'] = country
    #converting country names to correspond others in database
    df.to_csv('D:\DP-data\Converted_Data_Sources\\' + term + '.csv')

    
