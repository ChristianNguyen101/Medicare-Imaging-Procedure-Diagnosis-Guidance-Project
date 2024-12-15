# Medicare Imaging Procedure Diagnosis Guidance Project
This is a project that looks to address the need to align Clinical Intent with Medicare Reinbursement Guidelines. 

When ordering imaging procedure for patients, medical providers may not have an up to date knowledge of the ordering diagnoses that provide coverage per CMS guidances. For example, ordering diagnosis I67.89 (Other cerebrovascular disease) meets medical necessity for Procedure Code 93880 (Non-Invasive Cerebrovascular Arterial Studies) but ordering I67.9 (Cerebrovascular disease, unspecified) does not. 

Ordering imaging with the incorrect procedure codes may result in denied claims, causing patients to face unexpected out-of-pocket expenses or delays in receiving necessary medical procedures. It also presents an administrative burden as healthcare providers and staff may need to spend additional time correcting errors, resubmitting claims, and communicating with insurance companies to resolve coding discrepancies. 

This project aims to reduce ambiguity in ordering diagnosis coverage by data scraping publicly available guidances from CMS sites such as https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleId=52992&ver=22. The program will scrape and store the ordering diagnoses that meet necessity. When a medical provider enters a procedure code and ordering diagnosis, the program will then compare the ordering diagnosis with the stored data and alert the provider if the code is not covered under Medicare (code is not found in the stored data). Finally, the program will prompt the user with similar codes that are covered by Medicare. 

Completed Steps: 
