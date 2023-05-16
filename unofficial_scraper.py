import os
import re

import pandas as pd
import pdfplumber

precinct_re = re.compile(r'\d{4}')
# results_re = re.compile(r'(\d+) (\d+\.\d\d%) (\d+) (\d+) (\d+)')
results_re = re.compile(r'(\d+) (\d+) (\d+) (\d+)')
fullName_re = re.compile(r'([A-Za-z-". ]+)')

raceName = None
votePercentage = None
name = None
precinct = None

resultsList = []

def get_results(text):
    for i, line in enumerate(text.split('\n')):
        # This works
        if 'Vote For 1' in line:
            raceName = text.split('\n')[i-1]
            # print(raceName)
        
        # This works
        if precinct_re.match(line):
            precinct = line[0:4]
            # print(precinct)

        # print(i, line)
        match = results_re.search(line)
        if (match and 'Ballots Cast' not in line):
            name = fullName_re.search(line).group(1)
            voteTotal = match.group(1)
            resultsList.append(
                {
                    'precinct': precinct,
                    'raceName': raceName,
                    'name': name,
                    'voteTotal': voteTotal
                }
            )

        # if (results_re.search(line) and 'Total Votes' not in line):
        #     name = fullName_re.search(line).group(1)
        #     print(name)
        #     voteTotal = results_re.search(str(line)).group(1)
        #     print(voteTotal)
            # resultsList.append(
            #     {
            #         'precinct': precinct,
            #         'raceName': raceName,
            #         'name': name,
            #         'voteTotal': voteTotal
            #     }
            # )

with pdfplumber.open(os.path.join(os.getcwd(), 'source_pdfs/may_24_repub.pdf')) as pdf:
    for page in pdf.pages:
        print(page)
        try:
            get_results(page.extract_text())
        except:
            pass
        # get_results(page.extract_text())


df = pd.DataFrame(resultsList)
df.to_csv('data/may_24_repub.csv', index=False)
print(df)

