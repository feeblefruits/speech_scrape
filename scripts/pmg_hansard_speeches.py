
# coding: utf-8

# from google.colab import drive , files
import re
import pandas as pd
import requests
import json
from datetime import datetime as dt
from bs4 import BeautifulSoup

headers = {
    'Content-Type': 'application/json',
}
collection = [] #store list of all collected hansard speeches
#   crawl though available pages
def get_data():
    base_url = "https://api.pmg.org.za/hansard/?page="

    for page in range(1, 100,1):
        url = base_url+str(page)
        resp = requests.get(url, headers=headers)
        data = resp.json()
        all_hansards = data['results']
        next_link = data['next']
        if next_link is not None:
            # collect hansard details from each page
            for hansard in all_hansards:
                d = {}
                d["title"] = hansard["title"]
                d["date"] = hansard["date"]
                d["speech"]  = hansard['body']
                #   collect data in a list
                collection.append(d)
        else:
            break
    return collection

def clean_hansards():
    df_raw = pd.DataFrame(get_data())
    cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|[\n\r\t]")

    df_raw['date'] = df_raw['date'].apply(lambda d: pd.to_datetime(d).strftime('%d-%b-%Y'))
    df_raw['speech'] = df_raw['speech'].astype(str).apply(lambda d: re.sub(cleanr, " ", d))
    df_raw['speech'] = df_raw['speech'].apply(lambda x: ' '.join(x.split()).strip())
    df_raw['title'] = df_raw['title'].astype(str).apply(lambda x: ' '.join(x.split()).strip())
    # df_raw['speech'].apply(lambda d: BeautifulSoup(d).text.strip())
#     print(df_raw.head(2))

    return df_raw

def create_title(clean_hansards):
    df_raw['name'] = df_raw['date'].astype(str) +' - '+ df_raw['title']
    # df_raw['name'] = df_raw['name'].apply(lambda x : x[:200].strip())
    df_hans = df_raw[['name', 'speech']]
#     print (df_hans.head(2))
    return df_hans

## Export to TXT files

def save_to_file(p):
    file_path = '../hansard_speeches/'  # Change path to suit local dir
    i = 0
    for index, row in p.iterrows():
        if i > len(p):
            break
        else:
            if len(row[0]) > 200:
                row[0]= row[0][:150]
            else:
                f = open(file_path+row[0]+'.txt','w+')
                f.write(row[1])
                f.close()
                i+=1

p = create_title(clean_hansards)

## save the txt file to local drive
save_to_file(p)