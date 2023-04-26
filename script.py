import requests
from bs4 import BeautifulSoup
import csv

url = 'https://attack.mitre.org/groups/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


groups_table = soup.find('table')
rows = groups_table.find_all('tr')

output = []
count = 0

for row in rows[1:]:
    group_name = row.find_all('td')[1].find('a').text
    
    count += 1
    print(count, group_name)
    
    techniques_url = row.find('td').find('a')['href']
    techniques_url = "https://attack.mitre.org" + techniques_url
    print(techniques_url)
    techniques_response = requests.get(techniques_url)
    techniques_soup = BeautifulSoup(techniques_response.text, 'html.parser')

    
    techniques_table = techniques_soup.find('table', {'class': 'techniques-used'})
    if techniques_table != None: 
        techniques_rows = techniques_table.find_all('tr')

        for technique_row in techniques_rows[1:]:

            technique_domain = technique_row.find_all('td')[0].text.strip()
            technique_id = technique_row.find_all('td')[1].text.strip()
            technique_name = technique_row.find_all('td')[2].text.strip()
            technique_desc = technique_row.find_all('td')[3].text.strip()

            if "CVE" in technique_desc: 
                specific_techniques_url = technique_id = technique_row.find_all('td')[1].find('a')['href']

                if specific_techniques_url: 
                    specific_techniques_url = "https://attack.mitre.org" + specific_techniques_url
                tactic_response = requests.get(specific_techniques_url)
                tactic_soup = BeautifulSoup(tactic_response.text, 'html.parser')
                
                for i in tactic_soup.find_all('span', {'class': "h5 card-title"}):
                    if "Tactic:" in i: 
                        tactic_name = i.find_next('a').text


                technique_info = [group_name[0:-1]] + [technique_domain] + [technique_id[-5:]] + ["Tactic: " + tactic_name] + ["Technique: " + technique_name] + [technique_desc]
                output.append(technique_info)

output.insert(0, ["group_name"] + ["technique_domain"] + ["technique_id"] + ["tactic_name"] + ["technique_name"] + ["technique_desc"])

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output)