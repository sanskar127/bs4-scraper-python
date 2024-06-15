import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Function to scrape table data
def scrape_table(url):
    # Use requests to fetch initial page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the total number of pages (if available)
    # This depends on how pagination is implemented on the website
    total_pages = 10  # Example: set the total number of pages

    table_data = []
    headers = []

    # Loop through each page
    for page in range(1, total_pages + 1):
        if page > 1:
            # Use Selenium for dynamic content on subsequent pages
            driver = webdriver.Chrome()  # Change to your WebDriver and its path
            driver.get(url)
            try:
                # Wait for the pagination link to be clickable
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, str(page)))
                )
                element.click()
                time.sleep(3)  # Adjust the sleep time as needed to ensure page loads fully
                soup = BeautifulSoup(driver.page_source, 'html.parser')
            finally:
                driver.quit()

        # Extract table data from the current page
        table = soup.find('table')
        if table:
            for row_idx, row in enumerate(table.find_all('tr')):
                row_data = []
                for col_idx, cell in enumerate(row.find_all(['th', 'td'])):
                    if row_idx == 0:
                        headers.append(cell.text.strip())
                    else:
                        row_data.append(cell.text.strip())
                if row_data:
                    table_data.append(row_data)

    return headers, table_data

# Function to save data to JSON file
def save_to_json(headers, table_data, filename):
    data = {
        "headers": headers,
        "table_data": table_data
    }
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
url = 'https://pcsx2.net/compat'  # Replace with your URL
headers, table_data = scrape_table(url)

# Save scraped data to JSON file
json_filename = 'scraped_data.json'
save_to_json(headers, table_data, json_filename)
print(f"Scraped data saved to {json_filename}")
