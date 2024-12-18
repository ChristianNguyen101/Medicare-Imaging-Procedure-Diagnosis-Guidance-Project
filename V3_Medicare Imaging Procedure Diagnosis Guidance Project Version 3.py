#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 11:02:56 2024

@author: christian_nguyen
"""

import requests
from bs4 import BeautifulSoup
from rich import print
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from difflib import get_close_matches

# Define the search query
Procedure_query = input("Enter your procedure: ")
diagnosis_query = input("Enter your diagnosis: ")
P_query = f"cms billing guidelines for {Procedure_query}"
D_query = f"{diagnosis_query} ICD-10 code"
P_url = f"https://www.google.com/search?q={P_query}"
D_url = f"https://www.google.com/search?q={D_query}"

#Headless Mode
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

# Initialize the driver
driver = webdriver.Chrome(options=options)

# Get the website
driver.get(D_url)


# Initialize WebDriverWait
wait = WebDriverWait(driver, 10)

xpaths = [
    '//mark',  # Original XPath
    '//span[contains(text(), "ICD-10")]',  # Alternative XPath
    '//div[contains(@class, "BNeawe") and contains(text(), "ICD-10")]',  # Broadest XPath
]

icd_code = None
for xpath in xpaths:
    try:
        icd_code_element = wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        icd_code = icd_code_element.text
        break  # Exit loop if code is found
    except Exception:
        continue  # Try the next XPath

# Print the result
if icd_code:
    print(f"[bold blue]ICD-10 Code Found:[/bold blue] {icd_code}")
else:
    print("[red]Failed to find ICD-10 code with provided XPaths![/red]")
    
if icd_code:
    user_input = input(f"Is the ICD-10 code '{icd_code}' correct? (yes/no): ").strip().lower()
    if user_input =='yes':
        icd_code = input("Please confirm the correct ICD-10 code: ").strip()
    if user_input == 'no':
        icd_code = input("Please input the correct ICD-10 code: ").strip()
    print(f"[bold green]Final ICD-10 Code:[/bold green] {icd_code}")
else:
    icd_code = input("No code was found. Please input the ICD-10 code manually: ").strip()
    print(f"[bold green]Final ICD-10 Code:[/bold green] {icd_code}")    

# Set headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send the request
response = requests.get(P_url, headers=headers)

# Parse the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

def extract_results(soup):
    # Identify the main container for results
    main = soup.select_one("#main")
    if not main:
        return []

    res = []
    # Loop through each result container
    for gdiv in main.select('.g'):
        result = extract_section(gdiv)
        if result:
            res.append(result)
    return res

def extract_section(gdiv):
    # Extract elements from the container
    title_element = gdiv.select_one('h3')
    link_element = gdiv.select_one('a')
    description_element = gdiv.select_one('.VwiC3b')  # Adjusted for Google's description class
    
    # Build the result dictionary
    return {
        'title': title_element.text if title_element else None,
        'link': urljoin("https://www.google.com", link_element['href']) if link_element else None,
        'description': description_element.text if description_element else None
    }

# Extract results
results = extract_results(soup)

# Print only the first result
if results:
    first_result = results[0]
    print("[bold green]First Billing Guidance Result[/bold green]:")
    print(f"Title: {first_result['title']}")
    print(f"Link: {first_result['link']}")
    print(f"Description: {first_result['description']}")
else:
    print("[red]No results found![/red]")

first_link = first_result['link']

# Get the website
driver.get(first_link)


# Initialize WebDriverWait
wait = WebDriverWait(driver, 10)
     
#Click the "Accept License" button
auto_element = wait.until(EC.element_to_be_clickable((By.ID, "btnAcceptLicense")))
auto_element.click()

table_Xpath = '//*[@id="gdvIcd10CoveredCodes1"]/tbody/'

test = driver.find_elements(By.XPATH, table_Xpath +'tr')

num_rows = len(driver.find_elements(by='xpath', value=table_Xpath + 'tr')) + 1
num_cols = len(driver.find_elements(by='xpath', value=table_Xpath + 'tr[1]/td'))


table_data=[]

for row in test:
        cells = row.find_elements(By.TAG_NAME,'td')
        cell_texts = [cell.text for cell in cells]
        table_data.append(cell_texts)
        print(" | ".join(cell_texts))
        
user_icd_code = icd_code.strip()  # Ensure no extra spaces in user input
matches_found = [row for row in table_data if user_icd_code in row]

if matches_found:
    print(f"[bold green]Exact Match Found![/bold green] The ICD-10 code '{user_icd_code}' is covered under Medicare Billing Guidelines")
    print("[bold green]Matched Code:[/bold green]")
    for match in matches_found:
        print(" | ".join(match))  # Print the entire matched row
else:
    print(f"[bold red]No Exact Match Found![/bold red] The ICD-10 code '{user_icd_code}' is not covered under Medicare Billing Guidelines.")
    
    # Extract all ICD-10 codes from the table data (assuming they are in the first column)
    all_codes = [row[0] for row in table_data if row]  # Ensure row is not empty
    
    # Get the closest matches
    close_matches = get_close_matches(user_icd_code, all_codes, n=5, cutoff=0.6)
    
    if close_matches:
        print(f"[bold yellow]Would one of these covered diagnoses match clinical presentation?[/bold yellow]")
        for match in close_matches:
            # Find and print the matched row for each close match
            matched_row = next((row for row in table_data if row[0] == match), None)
            if matched_row:
                print(f"  - [bold cyan]ICD-10 Code:[/bold cyan] {match}")
                print(f"    [bold cyan]Details:[/bold cyan] {' | '.join(matched_row)}")
    else:
        print("[bold red]No similar codes found![/bold red]")