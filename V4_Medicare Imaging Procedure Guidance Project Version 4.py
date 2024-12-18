import tkinter as tk
from tkinter import simpledialog, messagebox
from rich import print
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from difflib import get_close_matches


class ICD10GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ICD-10 Ordering Diagnosis Program")
        self.root.geometry("800x600")

        # Procedure Input
        tk.Label(root, text="Procedure:", font=("Arial", 24, "bold")).pack(pady=10)
        self.procedure_entry = tk.Entry(root, font=("Arial", 20), width=50)
        self.procedure_entry.pack(pady=5)

        # Diagnosis Input
        tk.Label(root, text="Diagnosis:", font=("Arial", 24, "bold")).pack(pady=10)
        self.diagnosis_entry = tk.Entry(root, font=("Arial", 20), width=50)
        self.diagnosis_entry.pack(pady=5)

        # Submit Button
        tk.Button(root, text="Run Process", command=self.run_process, font=("Arial", 20)).pack(pady=20)

        # Log Output
        self.log_output = tk.Text(root, font=("Courier", 16), width=70, height=15, wrap="word")
        self.log_output.pack(pady=10)

        # Add color tags to log_output
        self.log_output.tag_config("bold_blue", foreground="blue", font=("Courier", 16, "bold"))
        self.log_output.tag_config("bold_green", foreground="green", font=("Courier", 16, "bold"))
        self.log_output.tag_config("bold_red", foreground="red", font=("Courier", 16, "bold"))
        self.log_output.tag_config("bold_yellow", foreground="orange", font=("Courier", 16, "bold"))
        self.log_output.tag_config("bold_cyan", foreground="cyan", font=("Courier", 16, "bold"))

    def log(self, message, tag=None):
        """Log messages to the text widget with optional colors."""
        if tag:
            self.log_output.insert(tk.END, f"{message}\n", tag)
        else:
            self.log_output.insert(tk.END, f"{message}\n")
        self.log_output.see(tk.END)

    def run_process(self):
        """Run the process for ICD-10 and billing guidelines."""
        procedure = self.procedure_entry.get().strip()
        diagnosis = self.diagnosis_entry.get().strip()

        if not procedure or not diagnosis:
            messagebox.showerror("Error", "Both Procedure and Diagnosis fields are required.")
            return

        P_query = f"cms billing guidelines for {procedure}"
        D_query = f"{diagnosis} ICD-10 code"
        P_url = f"https://www.google.com/search?q={P_query}"
        D_url = f"https://www.google.com/search?q={D_query}"

        # Selenium Headless Mode
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

        try:
            # Get ICD-10 Code
            driver.get(D_url)
            wait = WebDriverWait(driver, 10)

            xpaths = [
                '//mark',
                '//span[contains(text(), "ICD-10")]',
                '//div[contains(@class, "BNeawe") and contains(text(), "ICD-10")]',
            ]

            icd_code = None
            for xpath in xpaths:
                try:
                    icd_code_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    icd_code = icd_code_element.text
                    break
                except Exception:
                    continue

            if icd_code:
                self.log(f"ICD-10 Code Found: {icd_code}", "bold_blue")
            else:
                self.log("Failed to find ICD-10 code with provided XPaths!", "bold_red")

            # User must confirm and re-input the ICD-10 code
            icd_code = simpledialog.askstring("Confirm ICD-10 Code", "Please re-input the ICD-10 code:")
            if not icd_code:
                messagebox.showerror("Error", "ICD-10 code is required.")
                return

            self.log(f"Final ICD-10 Code: {icd_code}", "bold_green")

            # Fetch Billing Guidance Results
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(P_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            def extract_results(soup):
                main = soup.select_one("#main")
                if not main:
                    return []

                res = []
                for gdiv in main.select('.g'):
                    title_element = gdiv.select_one('h3')
                    link_element = gdiv.select_one('a')
                    description_element = gdiv.select_one('.VwiC3b')

                    res.append({
                        'title': title_element.text if title_element else None,
                        'link': urljoin("https://www.google.com", link_element['href']) if link_element else None,
                        'description': description_element.text if description_element else None,
                    })
                return res

            results = extract_results(soup)
            if results:
                first_result = results[0]
                self.log("First Billing Guidance Result Found.", "bold_green")
            else:
                self.log("No results found!", "bold_red")
                return

            # Access Billing Table
            first_link = first_result['link']
            driver.get(first_link)

            # Accept License
            try:
                accept_button = wait.until(EC.element_to_be_clickable((By.ID, "btnAcceptLicense")))
                accept_button.click()
            except Exception:
                self.log("No license button found.", "bold_yellow")

            # Fetch Table Data
            table_xpath = '//*[@id="gdvIcd10CoveredCodes1"]/tbody/tr'
            rows = driver.find_elements(By.XPATH, table_xpath)

            table_data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                cell_texts = [cell.text for cell in cells]
                table_data.append(cell_texts)

            # Log matches
            self.log("Checking ICD-10 Code Matches:", "bold_green")
            matches = [row for row in table_data if icd_code in row]
            if matches:
                self.log(f"ICD-10 Code '{icd_code}' is covered under Medicare guidelines!:", "bold_green")
                for match in matches:
                    self.log(" | ".join(match), "bold_green")
            else:
                self.log(f"ICD-10 Code '{icd_code}' is not covered under Medicare guidelines!", "bold_red")
                # Find close matches
                all_codes = [row[0] for row in table_data if row]
                close_matches = get_close_matches(icd_code, all_codes, n=5, cutoff=0.6)
                if close_matches:
                    self.log("These covered codes may match clinical presentation:", "bold_yellow")
                    for match in close_matches:
                        matched_row = next((row for row in table_data if row[0] == match), None)
                        if matched_row:
                            self.log(" | ".join(matched_row), "bold_yellow")
                else:
                    self.log("No similar codes found!", "bold_red")

        finally:
            driver.quit()


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ICD10GUI(root)
    root.mainloop()
