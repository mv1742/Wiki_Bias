# Script

# Script only runs in Python 2


# Having SECEdgar package downloaded from GitHub is essential for this plot

# If it is installed from PyPI (aka using pip install command), run the following line to delete it:
# !pip uninstall SECEdgar

# Run the following three lines to install from GitHub:
# !git clone https://github.com/rahulrrixe/SEC-Edgar.git
# !cd SEC-Edgar
# !python setup.py install

# Import packages used in the script
from SECEdgar.crawler import SecCrawler
import csv

# Define global variable
secCrawler = SecCrawler()


# Function to download all 10-K filings starting from the year inputed
def fake_function_10k_v2(year, cik, companycode):
    global seccrawler
    companyCode = str(ticker)
    cik = str(cik_file)
    date = str(year) + '12' + '31'
    count = '100'
    SecCrawler().filing_10K(companyCode, cik, date, count)


# import file
file = open('companies.csv')
csv_file = csv.DictReader(file)

# Call function for every row in the file
for row in csv_file:
    year = 1980
    cik_file = row['cik']
    ticker = row['ticker']
    while year < 2018:
        year += 1
        fake_function_10k_v2(year, cik_file, ticker)
    year = 1980
