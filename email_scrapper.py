#!/usr/bin/python

from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

google_search_client_list_csv_data = pd.read_csv('./input.csv', on_bad_lines='warn')
search_results = []
chunk_size = 50

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, num=1, **kwargs).execute()
    return res

def findEmailsInText(text):
    return re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z0-9\.\-+_]+", text, re.I)

def generateChunks(listToChunk, chunkSize):
    for i in range(0, len(listToChunk), chunkSize):
        yield listToChunk[i:i+chunkSize]

def getURLFromText(term):
    try:
        result = google_search(term, os.environ['GOOGLE_API_KEY'], os.environ['GOOGLE_CSE_ID'])
        if len(result['items']) > 0:
            return result['items'][0]['link']
        for url in search(term, num_results=1):
            return url
        return ''
    except Exception as ex: print(ex)

def scrapEmails(input):
    emails = []
    privacy_links_to_check = 0
    other_links_to_check = 0
    try:
        result_web_url = getURLFromText(input)
        print('\nFinding emails for ', result_web_url, 'using search text:', input, '\n')
        if result_web_url is not None and len(result_web_url) > 0:
            response = requests.get(result_web_url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            emails.extend(x for x in findEmailsInText(response.text) if x not in emails)

            for page_data in soup.find_all('a'):
                link = page_data.get('href')
                if link is not None and 'http' not in link:
                    link = result_web_url + link
                if link is not None and ('privacy' in link) and privacy_links_to_check <= 5:
                    privacy_links_to_check += 1
                    page_response = requests.get(link, timeout=5)
                    emails.extend(x for x in findEmailsInText(page_response.text) if x not in emails)
                elif link is not None and ('privacy' in link or 'contact' in link or 'about' in link) and other_links_to_check <= 3:
                    other_links_to_check += 1
                    page_response = requests.get(link)
                    emails.extend(x for x in findEmailsInText(page_response.text) if x not in emails)
                elif privacy_links_to_check == 5 and other_links_to_check == 3:
                    break

        print('Result: ', emails)
        return {
            'url': result_web_url,
            'emails': emails
        }

    except IOError:
        print(("No results found!"+""))
        return {}

chunks = generateChunks(google_search_client_list_csv_data, chunk_size)

for chunk in chunks:
    for index, row in chunk.iterrows():
        scrap_result = scrapEmails(row.get('Company Name'))
        search_results.append({
            'COMPANY_NAME': row.get('Company Name'),
            'URL': scrap_result.get('url'),
            'CONTACT_EMAIL': scrap_result.get('emails')
        })
    print('Search completed, writing to csv file')
    search_results_df = pd.DataFrame.from_dict(search_results)
    search_results_df.to_csv (r'./output/output' + str(index) + '.csv', index = False, header=True)