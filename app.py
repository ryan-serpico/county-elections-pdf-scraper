import os
import re

import pandas as pd
import pdfplumber

# Name of the file you want to scrape
FILENAME = "fall_2022_bexar_precinct_results.pdf"
OUTPUT_FILENAME = "2022_general.csv"

# Define regular expressions to match patterns in the text
precinct_re = re.compile(r"\d{4}")
results_re = re.compile(r"(\d+) (\d+\.\d\d%) (\d+) (\d+) (\d+)")
fullName_re = re.compile(r'([A-Za-z-". ]+)')
electionRace = re.compile(r"^For .+")

# Initialize variables
raceName = None
votePercentage = None
name = None
precinct = None
resultsList = []


# Define function to extract results from text
def get_results(text):
    for i, line in enumerate(text.split("\n")):
        # Find the name of the race
        if "Vote For 1" in line:
            raceName = text.split("\n")[i - 1]

        # Find the precinct number
        if precinct_re.match(line):
            precinct = line[0:4]

        # Find the results for a candidate
        if results_re.search(line) and "Total Votes" not in line:
            name = fullName_re.search(line).group(1)
            votePercentage = results_re.search(str(line)).group(2)
            resultsList.append(
                {
                    "precinct": precinct,
                    "raceName": raceName,
                    "name": name,
                    "votePercentage": votePercentage,
                }
            )


def extract_results(filename: str, output_filename: str) -> None:
    # Check to see if there's a folder for the source PDFs
    if not os.path.exists("source_pdfs"):
        os.makedirs("source_pdfs")
        print(
            "You need to put the source PDF into a folder titled 'source_pdfs'. I just created it for you. Add the PDF there and run this script again."
        )
        return

    # Check to see if there's a folder for the output CSVs
    if not os.path.exists("output"):
        os.makedirs("output")
        print(
            "You need to have an output folder for the CSVs. I just created it for you. Run this script again."
        )
        return

    # Open the PDF file and extract the results
    with pdfplumber.open(os.path.join(os.getcwd(), f"source_pdfs/{filename}")) as pdf:
        for page in pdf.pages:
            print(page)
            try:
                get_results(page.extract_text())
            except:
                print("🚨 error 🚨")
                pass

    # Convert the results to a pandas DataFrame and save to a CSV file
    df = pd.DataFrame(resultsList)
    df.to_csv(f"output/{output_filename}", index=False)


extract_results(FILENAME, OUTPUT_FILENAME)
