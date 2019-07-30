# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import requests
import re
import time

links = []

def get_speech_links(page_number):
    
    url = requests.get('https://www.gov.za/speeches?page=' + str(page_number))
    soup = BeautifulSoup(url.text, 'html.parser')
    
    content = soup.find('tbody')
    
    for link in content.find_all('a'):
        links.append('https://www.gov.za' + link.get('href'))

def get_content(speech_link):
    
    url = requests.get(speech_link)
    page_soup = BeautifulSoup(url.text, 'html.parser')
    
    # content
    ps = []

    for p in page_soup.find_all('p'):

        ps.append(p.text)

    content = '\n'.join(ps)
    
    return content

def get_name(speech_link):
    try:
        url = requests.get(speech_link)
        page_soup = BeautifulSoup(url.text, 'html.parser')

        # title
        title = page_soup.find('h1', id='page-title').text
        # remove all non-alphanumeric characters
        title = re.sub(r'\W+', ' ', title)

        # date
        date = page_soup.find('div', class_='field-item even').text
        date = re.sub(r'\W+', '-', date)

        name = str(date) + ' - ' + str(title)
        
        if len(name) > 200:
            name = name[:180]
        else:
            name = name
        
        return name
    except AttributeError:
        print('Failed with AttributeError')

def get_date(speech_link):
    
    url = requests.get(speech_link)
    page_soup = BeautifulSoup(url.text, 'html.parser')
    
    try:
        # date
        date = page_soup.find('div', class_='field-item even').text
        date = re.sub(r'\W+', '-', date)

        return date
    except AttributeError:
        print('Failed with AttributeError')

# get all speech documents from pages

for i in range(0, 610):
    
    # could be updated to automatically check for number of page links
    
    get_speech_links(i)

# grab all content from speech documents

for link in links:
    
    try:
        file_name = get_name(link)
        date = get_date(link)
        content = get_content(link)
        
        try:
            with open(r"C:\Users\jcoet\Projects\speeches\new_speeches\%s.txt" %file_name, "w", encoding='UTF-8') as text_file:
                text_file.write(content)
        except OSError:
            with open(r"C:\Users\jcoet\Projects\speeches\new_speeches\%s.txt" %date, "w", encoding='UTF-8') as text_file:
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
                with open(r"C:\Users\jcoet\Projects\speeches\new_speeches\%s.txt" %file_name, "w", encoding='UTF-8') as text_file:
                    text_file.write(content)
            except OSError:
                with open(r"C:\Users\jcoet\Projects\speeches\new_speeches\%s.txt" %date, "w", encoding='UTF-8') as text_file:
                    text_file.write(content)
        except requests.exceptions.ConnectionError:

            print('Connection Error')
            print('... trying agian after three seconds.')

