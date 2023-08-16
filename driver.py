import csv
import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException



# Path to the geckodriver executable
# To adjust file location, change the GECKODRIVER_PATH variable below to the file path
GECKODRIVER_PATH = 'C:\\Users\\wyatt\\Documents\\ritterProject'

# Path to the CSV file
# To adjust file location, change the CSV_FILE_PATH variable below to the file path
CSV_FILE_PATH = 'final.csv'

# Create a new Firefox driver instance
options = Options()
options.headless = True  # Run Firefox in headless mode (no GUI)
driver = webdriver.Firefox(options=options)


# Set the maximum time to wait for a page to load (in seconds)
PAGE_LOAD_TIMEOUT = 10

# File to log unreachable sites
LOG_FILE = 'unreachable_sites.txt'

# Read the CSV file
with open(CSV_FILE_PATH, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row

    # Iterate through the URLs
    for row in csv_reader:
        if len(row) < 1:
            print("Skipping empty row")
            continue

        url = row[0]

        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        try:
            parsed_url = urlparse(url)
        except Exception as e:
            print(f'Error parsing URL: {url}')
            continue

        if not parsed_url.netloc:
            print(f'Malformed URL: {url}')
            continue

        filename = f'{parsed_url.netloc.replace(":", "_")}.png'

        # Declare and assign the driver instance
        try:
            # Load the webpage with a maximum timeout
            driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            driver.get(url)

            # Take a screenshot
            driver.save_screenshot(filename)

            print(f'Screenshot saved for {url}')
        except TimeoutException as e:
            print(f'Timeout while loading {url}: {str(e)}')
            with open(LOG_FILE, 'a') as log_file:
                log_file.write(f'Timeout: {url}\n')
        except Exception as e:
            print(f'Error capturing screenshot for {url}: {str(e)}')
            with open(LOG_FILE, 'a') as log_file:
                log_file.write(f'Error: {url}\n')

# Quit the driver
driver.quit()

