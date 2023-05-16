import os
import re

import pandas as pd
import pdfplumber

precinct_re = re.compile(r'\d{4}')
# results_re = re.compile(r'(\d+) (\d+\.\d\d%) (\d+) (\d+) (\d+)')
results_re = re.compile(r'(\d+) (\d+) (\d+) (\d+)')
fullName_re = re.compile(r'([A-Za-z-". ]+)')
voter_turnout_re = re.compile(r'(Voter Turnout - Total) (\d+\.\d\d%)')

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


        match = voter_turnout_re.search(line)
        if match:
            # print(precinct)
            # print(match.group(2))
            resultsList.append(
                {
                    'precinct': precinct,
                    'turnoutPerc': match.group(2),
                }
            )

with pdfplumber.open(os.path.join(os.getcwd(), 'source_pdfs/may_7.pdf')) as pdf:
    for page in pdf.pages:
        print(page)
        try:
            get_results(page.extract_text())
        except:
            pass


df = pd.DataFrame(resultsList)
df.to_csv('data/may_7_turnout.csv', index=False)
print(df)

