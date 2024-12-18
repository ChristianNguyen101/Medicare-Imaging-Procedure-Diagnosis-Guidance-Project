# Medicare Imaging Procedure Diagnosis Guidance Project
This is a project that looks to address the need to align Clinical Intent with Medicare Reinbursement Guidelines. 

When ordering imaging procedure for patients, medical providers may not have an up to date knowledge of the ordering diagnoses that provide coverage per CMS guidances. For example, ordering diagnosis I67.89 (Other cerebrovascular disease) meets medical necessity for Procedure Code 93880 (Non-Invasive Cerebrovascular Arterial Studies) but ordering I67.9 (Cerebrovascular disease, unspecified) does not. 

Ordering imaging with the incorrect procedure codes may result in denied claims, causing patients to face unexpected out-of-pocket expenses or delays in receiving necessary medical procedures. It also presents an administrative burden as healthcare providers and staff may need to spend additional time correcting errors, resubmitting claims, and communicating with insurance companies to resolve coding discrepancies. 

This project aims to reduce ambiguity in ordering diagnosis coverage by data scraping publicly available guidances from CMS sites such as https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleId=52992&ver=22. The program will scrape and store the ordering diagnoses that meet necessity. When a medical provider enters a procedure code and ordering diagnosis, the program will then compare the ordering diagnosis with the stored data and alert the provider if the code is not covered under Medicare (code is not found in the stored data). Finally, the program will prompt the user with similar codes that are covered by Medicare. 

Checkpoint Completion: Steps 1-5 (All Steps) Completed!

Version 1: This version of the project scrapes the data from the CMS website utilizing the Selenium package under headless mode to prevent site pop-ups. Running the program outputs the rows and columns of the ICD10 covered codes as well as contents of the ICD-10 Covered Codes table.

Version 2: This version of the project builds on version 1 by incorporating user input functionality. The user is prompted to enter the procedure they wish to order. The program then utilizes the prompt to generate the CMS billing guidance link and extract the ICD-10 Covered Codes table.

Version 3: This version of the project contains all functional aspects of the project. The user is prompted to enter the procedure code and ordering diagnosis. The program then determines the ICD-10 code associated with the ordering diagnosis and asks the user to confirm the ICD-10 Code. After confirmation, the program determines whether the diagnosis code is covered under medicare guidelines. If the code is not covered, the program provides Medicare covered codes with similar values as the entered code as suggestions.

Version 4: This version of the project incorporates a Graphic User Interface (GUI) for the user. The user now uses a pop-up window to input the procedure code, ordering diagnosis, and ICD-10 confirmation and views the output in the window. 
