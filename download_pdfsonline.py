# Import required libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import os

# --- Setup headless Chrome browser ---
options = Options()
options.add_argument("--headless")      # Run browser in headless mode (no UI)
options.add_argument("--disable-gpu")   # Disable GPU acceleration (safe fallback)
driver = webdriver.Chrome(options=options)  # Launch Chrome with specified options

# --- Navigate to target website ---
url = "https://pcmaster.multimodalsolutions.net/"
driver.get(url)
time.sleep(5)  # Wait for the page to fully load (can be optimized with WebDriverWait)

# --- Find all image elements on the page ---
images = driver.find_elements(By.TAG_NAME, 'img')
print(f"Found {len(images)} images.")

# --- Prepare to store PDF links and create download folder ---
pdf_links = set()  # Use set to avoid duplicates
os.makedirs('pdfs', exist_ok=True)  # Create 'pdfs' folder if it doesn't exist

# --- Iterate through each image and attempt to extract PDF ---
for idx, img in enumerate(images):
    try:
        print(f"Clicking image {idx + 1}/{len(images)}...")

        # Scroll to image (some websites require hovering to activate elements)
        ActionChains(driver).move_to_element(img).perform()

        # Track open tabs before clicking
        before_tabs = driver.window_handles

        # Click the image
        img.click()
        time.sleep(2)  # Allow any navigation or tab opening to complete

        # Track open tabs after clicking
        after_tabs = driver.window_handles

        # If a new tab was opened, handle it
        if len(after_tabs) > len(before_tabs):
            new_tab = [tab for tab in after_tabs if tab not in before_tabs][0]
            driver.switch_to.window(new_tab)  # Switch to the new tab

            pdf_url = driver.current_url  # Get the URL of the new tab

            # Check if it's a PDF and not already downloaded
            if pdf_url.endswith('.pdf') and pdf_url not in pdf_links:
                print(f"Found PDF: {pdf_url}")
                pdf_links.add(pdf_url)

                try:
                    # Download the PDF
                    response = requests.get(pdf_url)
                    filename = pdf_url.split('/')[-1].split('?')[0] or f"file_{idx}.pdf"
                    filepath = os.path.join('pdfs', filename)

                    # Save the PDF to the 'pdfs' folder
                    with open(filepath, 'wb') as f:
                        f.write(response.content)

                    print(f"Downloaded: {filename}")
                except Exception as download_err:
                    print(f"Error downloading {pdf_url}: {download_err}")

            # Close the PDF tab and return to the original tab
            driver.close()
            driver.switch_to.window(before_tabs[0])

    except Exception as e:
        print(f"Error on image {idx + 1}: {e}")  # Log any errors that occur for each image

# --- Cleanup ---
driver.quit()
print(f"Done. Total PDFs downloaded: {len(pdf_links)}")
