#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 19:38:51 2024

@author: christian_nguyen
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Headless Mode
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

# Initialize the driver
driver = webdriver.Chrome(options=options)

# Get the website
driver.get("https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleId=52992&ver=22")

# Initialize WebDriverWait
wait = WebDriverWait(driver, 10)
    
#Click the "Accept License" button
auto_element = wait.until(EC.element_to_be_clickable((By.ID, "btnAcceptLicense")))
auto_element.click()

table_Xpath = '//*[@id="gdvIcd10CoveredCodes1"]/tbody/'

test = driver.find_elements(By.XPATH, table_Xpath +'tr')

num_rows = len(driver.find_elements(by='xpath', value=table_Xpath + 'tr')) + 1
num_cols = len(driver.find_elements(by='xpath', value=table_Xpath + 'tr[1]/td'))

print(num_rows)
print(num_cols)

for row in test[:]:  # Skip the first row (headers)
        cells = row.find_elements(By.TAG_NAME, 'td')
        cell_texts = [cell.text for cell in cells]
        print(" | ".join(cell_texts))
