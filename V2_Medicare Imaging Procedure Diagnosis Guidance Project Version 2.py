#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 11:02:56 2024

@author: christian_evelynnguyen
"""

import requests
from bs4 import BeautifulSoup
from rich import print
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Define the search query
user_query = input("Enter your procedure: ")
query = f"cms billing guidelines for {user_query}"
url = f"https://www.google.com/search?q={query}"

# Set headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send the request
response = requests.get(url, headers=headers)

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
    print("[bold green]First Result[/bold green]:")
    print(f"Title: {first_result['title']}")
    print(f"Link: {first_result['link']}")
    print(f"Description: {first_result['description']}")
else:
    print("[red]No results found![/red]")

first_link = first_result['link']
 
#Headless Mode
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

# Initialize the driver
driver = webdriver.Chrome(options=options)

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


