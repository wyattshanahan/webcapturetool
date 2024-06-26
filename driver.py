import csv
import os
from sys import argv # for arguments
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
extendReport, extendFileName, skipHead = False, False, False # initialise variables

# check for arguments
if len(argv) > 1:
	if (argv[1] == '-h') or (argv[1] == '-help') or (argv[1] == '--h'):
		print("Usage: python driver.py <csv file name>")
		exit()
	if len(argv) == 2:
		CSV_FILE_PATH = argv[1] # Path to the CSV file
else:
	exit("Error: no arguments provided.")
# check if file exists, if not exit with an error
if os.path.exists(CSV_FILE_PATH) == False:
    print("Error: File not found.")
    exit(1)
# print upper logo -- all pre-execution checks above here
if os.get_terminal_size()[0] >= 76: # if terminal is wide enough, print the fullsize logo
    print("*==========================================================================*")
    print("|  _    _      _     _____             _                _____           _  |")
    print("| | |  | |    | |   /  __ \           | |              |_   _|         | | |")
    print("| | |  | | ___| |__ | /  \/ __ _ _ __ | |_ _   _ _ __ ___| | ___   ___ | | |")
    print("| | |/\| |/ _ \ '_ \| |    / _` | '_ \| __| | | | '__/ _ \ |/ _ \ / _ \| | |")
    print("| \  /\  /  __/ |_) | \__/\ (_| | |_) | |_| |_| | | |  __/ | (_) | (_) | | |")
    print("|  \/  \/ \___|_.__/ \____/\__,_| .__/ \__|\__,_|_|  \___\_/\___/ \___/|_| |")
    print("|                               | |                                        |")
    print("|                               |_|                               v2024.04 |")
    print("*==========================================================================*")
else: # if too small, print the smaller logo/startmark
    print("=======================\nWebCaptureTool v2024.04\n=======================")
# Create a new Firefox driver instance
options = Options()
options.headless = True  # Run Firefox in headless mode (no GUI)
options.add_argument("--headless")
driver = webdriver.Firefox(options=options) #removed executable_path=GECKODRIVER_PATH as per selenium 4.6.0
httpW,httpsW,timeout,misc = 0,0,0,0 # initialise counters

# Set the maximum time to wait for a page to load (in seconds)
PAGE_LOAD_TIMEOUT = 10

# File to log unreachable sites
LOG_FILE = 'unreachable_sites.txt'

# Read the CSV file
with open(CSV_FILE_PATH, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    #next(csv_reader)  # Skip the header row NOTE: currently disabled, will be implemented as an option in a future version

    # Iterate through the URLs
    for row in csv_reader:
        url = row[0]

        if not url.startswith(('http://', 'https://')): # append https:// to the URL
            url = 'https://' + url

        try: # verify it is parseable
            parsed_url = urlparse(url)
        except Exception as e: # if an error occurs during the check, report it occurred and continue
            print(f'Error parsing URL: {url}')
            continue

        if not parsed_url.netloc: # if malformed, print error
            print(f'Malformed URL: {url}')
            continue

        filename = f'{parsed_url.netloc.replace(":", "_")}.png' # set filename for saving, replacing : with _

        try:
            # Load the webpage with a maximum timeout
            driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            driver.get(url)
            # Take a screenshot
            driver.save_screenshot(filename)
            print(f'Screenshot saved for {url}')
            httpsW += 1 # increment when success
        # if an exception occurs, try replacing https with http
        except Exception as e:
            try: # try with http, screenshot and report success if successful
                url = url.replace("https://", "http://")
                driver.get(url)
                driver.save_screenshot(filename)
                print(f'Screenshot saved for {url}')
                httpW += 1 # increment when successful
            # if page times out, report and log the exception
            except TimeoutException as e:
                print(f'Timeout while loading {url}: {str(e.msg)}')
                with open(LOG_FILE, 'a') as log_file:
                    log_file.write(f'Timeout: {url}\n')
            # if page fails to load, report and log the exception
                timeout += 1 # increment if timeout
            except Exception as e:
                misc += 1 # increment if miscellaneous exception
                if 'e=nssFailure' in e.msg:
                    print(f'Error capturing screenshot for {url}: nssFailure')
                    with open(LOG_FILE, 'a') as log_file:
                        log_file.write(f'nnsFailure: {url}\n')
                elif 'e=dnsNotFound' in e.msg:
                    print(f'Error capturing screenshot for {url}: DNS not found')
                    with open(LOG_FILE, 'a') as log_file:
                        log_file.write(f'DNS not found: {url}\n')
                elif 'e=redirectLoop' in e.msg:
                    print(f'Error capturing screenshot for {url}: Redirect Loop')
                    with open(LOG_FILE, 'a') as log_file:
                        log_file.write(f'Redirect Loop: {url}\n')
                elif 'e=connectionFailure' in e.msg:
                    print(f'Error capturing screenshot for {url}: Connection Failed')
                    with open(LOG_FILE, 'a') as log_file:
                        log_file.write(f'Connection Failure: {url}\n')
                else:
                    print(f'Error capturing screenshot for {url}: {str(e.msg)}')
                    with open(LOG_FILE, 'a') as log_file:
                        log_file.write(f'Error: {url}\n')
# Quit the driver
driver.quit()

print("Execution completed successfully!")
# print total sites done, total successes, https/http successes, and failures (total and timeout/other)
print("\n*====================*")
print(" Final Report        ")
print("                    ")
print(f" Total Processed: {httpW+httpsW+timeout+misc}  ")
print(f" Total Successful: {httpW+httpsW} ")
print(f" Total Failures: {httpW+httpsW}   ")
print("*====================*")

# use argument and give extra info if requested
if (extendReport):
    print("\n*====================*")
    print(" Extended Report        ")
    print(f" HTTPS: {httpsW}")
    print(f" HTTP: {httpW}")
    print(f" Timeout: {timeout}")
    print(f" Other Errors: {misc}")
    print("*====================*")
