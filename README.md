# PDF Scraper

This Python script automates the process of finding and downloading PDF files from a website.

It uses Selenium to simulate clicking image elements that open PDFs in new tabs, then downloads the files to your local machine.

---

## 🔧 Features

- Headless browser automation using Selenium
- Automatically finds and clicks images that link to PDFs
- Detects and switches to new tabs
- Downloads PDF files into a local folder
- Prevents duplicate downloads

---

## 🧰 Requirements

- Python 3.x
- Google Chrome
- ChromeDriver (matching your Chrome version)
- Python packages:
  - `selenium`
  - `requests`

Install dependencies with:

```bash
pip install selenium requests
