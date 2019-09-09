
# coding: utf-8

# from google.colab import drive , files
import re
import pandas as pd
import requests
import json
from datetime import datetime as dt
from bs4 import BeautifulSoup


url = "https://api.pmg.org.za/hansard"

headers = {
    'Content-Type': 'application/json',
}

base_url = "https://api.pmg.org.za/hansard/?page="
collection = [] #store list of all collected hansard speeches
cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|[\n\r\t]")
file_path = '/content/drive/My Drive/Colab_Notebooks/m_g/hansard_speeches/' # Change path to suit local dir


#   crawl though available pages
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
            # d["house_id"] = hansard["house_id"]
            # d["summary"] = hansard["summary"]
            # d["url"] = hansard["url"]
            # d["featured"] = hansard["featured"]
            # d["chairperson"] = hansard["chairperson"]
            # d["type"] = hansard["type"]
            # d["id"] = hansard["id"]
            # d["nid"] = hansard["nid"]
            # d["member_id"] = hansard["member_id"]
            # d["committee_id"] = hansard["committee_id"]
            # d["updated_at"] = hansard["updated_at"]
            d["title"] = hansard["title"]
            d["date"] = hansard["date"]
            # d["public_participation"] = hansard["public_participation"]
            # d["created_at"] = hansard["created_at"]
            # clean the text from the html tags
            # cleanr = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|[\n\r\t]")
            # body = hansard["body"]
            # d["speech"] = re.sub(cleanr, ' ', body)

            d["speech"]  = hansard['body']
            #   collect data in a list
            collection.append(d)
            #   store items data in a dataframe & save to csv
            # df = pd.DataFrame(collection) #.to_csv("data/pmg_hansards.csv")
    else:
        break


df_raw = pd.DataFrame(collection)

def clean_hansards():
    df_raw['date'] = df_raw['date'].apply(lambda d: pd.to_datetime(d).strftime('%d-%b-%Y'))
    df_raw['speech'] = df_raw['speech'].astype(str).apply(lambda d: re.sub(cleanr, " ", d))
    df_raw['speech'] = df_raw['speech'].apply(lambda x: ' '.join(x.split()).strip())
    df_raw['title'] = df_raw['title'].astype(str).apply(lambda x: ' '.join(x.split()).strip())
    # df_raw['speech'].apply(lambda d: BeautifulSoup(d).text.strip())
#     print(df_raw.head(2))

    return df_raw

def create_title():
    clean_hansards()
    df_raw['name'] = df_raw['date'].astype(str) +' - '+ df_raw['title']
    # df_raw['name'] = df_raw['name'].apply(lambda x : x[:200].strip())
    df_hans = df_raw[['name', 'speech']]
#     print (df_hans.head(2))
    return df_hans

## Export to TXT files

def save_to_file(p):
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



## save the txt file to local drive

save_to_file(df_hans)
