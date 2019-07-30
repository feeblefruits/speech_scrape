# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import requests
import re
import time

links = []

def get_speech_links(page_number):
    
    url = requests.get('https://www.polity.org.za/page/speeches/page:' + str(page_number))
    soup = BeautifulSoup(url.text, 'html.parser')

    contents = soup.find_all('div', class_='entry block-padded')
    
    for content in contents:
        for link in content.find_all('a'):
            links.append('https://www.polity.org.za' + link.get('href'))
def get_content(speech_link):
    
    try:
        url = requests.get(speech_link)
        page_soup = BeautifulSoup(url.text, 'html.parser')

        # content
        ps = []

        for p in page_soup.find_all('div', id='article_content_container'):

            ps.append(p.text)

        content = '\n'.join(ps)

        return content
    except requests.exceptions.ChunkedEncodingError:
        print('ChunkedEncodingError')

def get_name(speech_link):
    
    try:
        url = requests.get(speech_link)
        page_soup = BeautifulSoup(url.text, 'html.parser')

        # title
        title = page_soup.find('h1', id='article_headline').text
        title = re.sub(r'\W+', ' ', title)

        # date
        container = page_soup.find('div', class_='meta')
        container = container.find('div', class_='left').text
        date = re.sub(r'\W+', ' ', container)

        name = str(date) + ' - ' + str(title)
        
        if len(name) > 200:
            name = name[:180]
        else:
            name = name

        return name
    except AttributeError:
        print('Failed with AttributeError - requested element not found')

def get_date(speech_link):
    
    url = requests.get(speech_link)
    page_soup = BeautifulSoup(url.text, 'html.parser')
    
    try:
        # date
        container = page_soup.find('div', class_='meta')
        container = container.find('div', class_='left').text
        date = re.sub(r'\W+', ' ', container)

        return date
    except AttributeError:
        print('Failed with AttributeError - requested element not found')

# get all speech document links from page links

for i in range(0, 1357):
    get_speech_links(i)

# grab content from all speech documents

for link in links:
    
    try:
        
        file_name = get_name(link)
        date = get_date(link)
        content = get_content(link)
        
        try:
            with open(r"C:\Users\jcoet\Projects\speeches\polity_speeches\%s.txt" %file_name, "w", encoding='UTF-8') as text_file:
                text_file.write(content)
        except OSError:
            with open(r"C:\Users\jcoet\Projects\speeches\polity_speeches\%s.txt" %date, "w", encoding='UTF-8') as text_file:
                text_file.write(content)
    except requests.exceptions.ConnectionError:
        
        print('Connection Error')
        print('... trying agian after three seconds.')
        
        time.sleep(3)
        
        try:
            file_name = get_name(link)
            date = get_date(link)
            content = get_content(link)
        
            try:
                with open(r"C:\Users\jcoet\Projects\speeches\polity_speeches\%s.txt" %file_name, "w", encoding='UTF-8') as text_file:
                    text_file.write(content)
            except OSError:
                with open(r"C:\Users\jcoet\Projects\speeches\polity_speeches\%s.txt" %date, "w", encoding='UTF-8') as text_file:
                    text_file.write(content)
        except requests.exceptions.ConnectionError:

            print('Connection Error')
            print('... trying agian after three seconds.')

