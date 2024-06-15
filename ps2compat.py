import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_pcsx2_compatibility(url):
    # Initialize ChromeDriver (change the executable_path to where your chromedriver is located)
    driver = webdriver.Chrome(executable_path='chromedriver/chromedriver.exe')

    try:
        driver.get(url)
        time.sleep(5)  # Let the page load completely (adjust as necessary)

        # Find the table element
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#compat_list_wrapper table')))
        
        # Get the page source
        page_source = driver.page_source
        
    finally:
        driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract table data
    table = soup.find('table', {'id': 'compat_list'})
    if not table:
        raise Exception("Table not found on the page")

    headers = [header.text.strip() for header in table.find_all('th')]
    table_data = []

    for row in table.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all('td')]
        if row_data:
            table_data.append(row_data)

    return headers, table_data

# Example usage
url = 'https://pcsx2.net/compat/'
headers, table_data = scrape_pcsx2_compatibility(url)

# Save scraped data to JSON file
json_filename = 'pcsx2_compatibility.json'
data = {
    "headers": headers,
    "table_data": table_data
}
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"Scraped data saved to {json_filename}")
