from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  # Import NoSuchElementException
import requests
from tqdm import tqdm

# ... rest of your code ...


# Function to get the href element using Selenium
def get_href_element(url):
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        element = driver.find_element(by=By.PARTIAL_LINK_TEXT, value="Download Preview")
        return element.get_attribute('href')
    except NoSuchElementException:
        print("Download link not found on the page.")
        return None

# Function to download a file using requests
def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        content_length = int(response.headers["Content-Length"])
        with open(filename, "wb") as f:
            for chunk in tqdm(response.iter_content(chunk_size=1024), unit="KB", total=content_length / 1024):
                f.write(chunk)

# Read codes from the output.txt file
with open("output.txt", "r") as f:
    codes = f.read().splitlines()

# Iterate over the codes and process each one
for code in codes:
    url = f'https://videohive.net/item/digital-logo-reveal/{code}'
    href = get_href_element(url)
    
    if href is not None:
        download_file(href, f'Videos/{code}.mp4')
        print(f"Downloaded video for code {code}")
    else:
        print(f"No download link found for code {code}")
