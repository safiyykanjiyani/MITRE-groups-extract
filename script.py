import csv
import requests
from bs4 import BeautifulSoup

# fetch the HTML page containing the table
url = 'https://attack.mitre.org/groups/'
response = requests.get(url)

# parse the HTML using Beautiful Soup
soup = BeautifulSoup(response.text, 'html.parser')

# find the table element
table = soup.find('table')

# create a CSV file and write the table data to it
with open('table.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            row_data.append(cell.get_text().strip())
        writer.writerow(row_data)