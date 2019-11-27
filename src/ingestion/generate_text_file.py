# Script to generate url links to be downloaded from enwiki

import requests

# Parsing HTML
from bs4 import BeautifulSoup

# File system management
import os
base_url = 'https://dumps.wikimedia.org/enwiki/'
index = requests.get(base_url).text
soup_index = BeautifulSoup(index, 'html.parser')

# Find the links that are dates of dumps
dumps = [a for a in soup_index.find_all('a')]

dump_url = base_url + 'latest/'

# Retrieve the html
dump_html = requests.get(dump_url).text


# Convert to a soup
soup_dump = BeautifulSoup(dump_html, 'html.parser')

# Find li elements with the class file
soup_dump.find_all('li', {'class': 'file'}, limit = 10)[:4]
files = []

# Search through all files
for file in soup_dump.find_all('li', {'class': 'file'}):
    text = file.text
    # Select the relevant files
    if 'stub-meta-history' in text:
        files.append((text.split()[0], text.split()[1:]))
        
# Download meta-stub historic Wikipedia
files_to_download_historic = [file[0] for file in files if '.gz' in file[0]]

url = 'https://dumps.wikimedia.org/enwiki/latest/'
files_to_download_url = [url+ i for i in files_to_download_historic]

with open('/home/ubuntu/Wiki_Bias/src/ingestion/enwiki-meta-history.txt', 'w+') as f:
    for item in files_to_download_url:
        f.write("%s\n" % item)

# Download current Wikipedia
for file in soup_dump.find_all('li', {'class': 'file'}):
    text = file.text
    # Select the relevant files
    if 'pages-articles-multistream' in text:
        files.append((text.split()[0], text.split()[1:]))

# files
files_to_download_current = [file[0] for file in files if '.bz2' in file[0]]
files_to_download_url = [url+ i for i in files_to_download_current]

with open('/home/ubuntu/Wiki_Bias/src/ingestion/enwiki-pages-mutlistream.txt', 'w+') as f:
    for item in files_to_download_url:
        f.write("%s\n" % item)