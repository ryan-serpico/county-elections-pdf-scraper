import os
import re

import pandas as pd
import pdfplumber

precinct_re = re.compile(r'\d{4}')
results_re = re.compile(r'(\d+) (\d+\.\d\d%) (\d+) (\d+) (\d+)')
fullName_re = re.compile(r'([A-Za-z-". ]+)')
electionRace = re.compile(r'^For .+')

raceName = None
votePercentage = None
name = None
precinct = None

resultsList = []

def get_results(text):
    for i, line in enumerate(text.split('\n')):
        if 'Vote For 1' in line:
            raceName = text.split('\n')[i-1]
        
        if precinct_re.match(line):
            precinct = line[0:4]

        if (results_re.search(line) and 'Total Votes' not in line):
            name = fullName_re.search(line).group(1)
            votePercentage = results_re.search(str(line)).group(2)
            resultsList.append(
                {
                    'precinct': precinct,
                    'raceName': raceName,
                    'name': name,
                    'votePercentage': votePercentage
                }
            )

with pdfplumber.open(os.path.join(os.getcwd(), 'may_7_2022.pdf')) as pdf:
    for page in pdf.pages:
        print(page)
        try:
            get_results(page.extract_text())
        except:
            pass


df = pd.DataFrame(resultsList)
df.to_csv('may_7_2022.csv', index=False)
print(df)

