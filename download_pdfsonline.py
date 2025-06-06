from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import os

# Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

url = "https://pcmaster.multimodalsolutions.net/"
driver.get(url)
time.sleep(5)

# Find all image elements
images = driver.find_elements(By.TAG_NAME, 'img')
print(f"Found {len(images)} images.")

pdf_links = set()
os.makedirs('pdfs', exist_ok=True)

for idx, img in enumerate(images):
    try:
        print(f"Clicking image {idx + 1}/{len(images)}...")
        ActionChains(driver).move_to_element(img).perform()

        # Track tabs before click
        before_tabs = driver.window_handles

        img.click()
        time.sleep(2)

        after_tabs = driver.window_handles

        # If a new tab was opened
        if len(after_tabs) > len(before_tabs):
            new_tab = [tab for tab in after_tabs if tab not in before_tabs][0]
            driver.switch_to.window(new_tab)
            pdf_url = driver.current_url

            if pdf_url.endswith('.pdf') and pdf_url not in pdf_links:
                print(f"Found PDF: {pdf_url}")
                pdf_links.add(pdf_url)

                try:
                    response = requests.get(pdf_url)
                    filename = pdf_url.split('/')[-1].split('?')[0] or f"file_{idx}.pdf"
                    filepath = os.path.join('pdfs', filename)
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded: {filename}")
                except Exception as download_err:
                    print(f"Error downloading {pdf_url}: {download_err}")

            # Close the PDF tab and return to main
            driver.close()
            driver.switch_to.window(before_tabs[0])

    except Exception as e:
        print(f"Error on image {idx + 1}: {e}")

driver.quit()
print(f"Done. Total PDFs downloaded: {len(pdf_links)}")
