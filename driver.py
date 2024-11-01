import csv
import os
from sys import argv # for arguments
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import datetime
extendReport, extendFileName, skipHead = False, False, False # initialise variables

#FUNCTION DEFINITIONS - IN ALPHABETICAL ORDER

def build_dir_name():
    current_time = datetime.datetime.now()
    formatted_date = current_time.strftime("%Y%m%d_%H%M%S")
    dir_name = "./" + formatted_date + "_screenshots"
    return dir_name

def display_logo(): # function to display the logo upon startup
    if os.get_terminal_size()[0] >= 76: # if terminal is wide enough, print the fullsize logo
        print("*==========================================================================*")
        print("|  _    _      _     _____             _                _____           _  |")
        print("| | |  | |    | |   /  __ \           | |              |_   _|         | | |")
        print("| | |  | | ___| |__ | /  \/ __ _ _ __ | |_ _   _ _ __ ___| | ___   ___ | | |")
        print("| | |/\| |/ _ \ '_ \| |    / _` | '_ \| __| | | | '__/ _ \ |/ _ \ / _ \| | |")
        print("| \  /\  /  __/ |_) | \__/\ (_| | |_) | |_| |_| | | |  __/ | (_) | (_) | | |")
        print("|  \/  \/ \___|_.__/ \____/\__,_| .__/ \__|\__,_|_|  \___\_/\___/ \___/|_| |")
        print("|                               | |                                        |")
        print("|                               |_|                               v2024.10 |")
        print("*==========================================================================*")
        return 0
    else: # if too small, print the smaller logo/startmark
        print("=======================\nWebCaptureTool v2024.04\n=======================")

def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        return 0
    else:
        exit("Error: directory already exists.")


def print_report(http, https, timeout, misc, extendReport):
    # print total sites done, total successes, https/http successes, and failures (total and timeout/other)
    print("\n*====================*")
    print(" Final Report        ")
    print(f"\n Total Processed: {http+https+timeout+misc}  ")
    print(f" Total Successful: {http+https} ")
    print(f" Total Failures: {timeout+misc}   ")
    print("*====================*")
    if (extendReport): #if extendReport is true, then print out detailed stats
        print("\n*====================*")
        print(" Extended Report        ")
        print(f" HTTPS: {https}")
        print(f" HTTP: {http}")
        print(f" Timeout: {timeout}")
        print(f" Other Errors: {misc}")
        print("*====================*")

def process_default_args(argv):
    if len(argv) > 1:
        if (argv[1] == '-h') or (argv[1] == '-help') or (argv[1] == '--h'):
            exit("Usage: python driver.py <csv file name>")
        if len(argv) == 2:
            if os.path.exists(argv[1]) == False: # check if file exists, exit if not else return the file path
                exit("Error: file not found.")
            else:
                return argv[1] # Path to the CSV file
    else: # exit if no args provided
        exit("Error: no arguments provided.")

def process_std_exceptions(LOG_FILE, e, url, timeout=None):
    if timeout == True: # if timeout error, then process and return timeout
        print(f'Timeout while loading {url}: {str(e.msg)}')
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f'Timeout: {url}\n')
        return "timeout" # if timeout error
    elif 'e=nssFailure' in e.msg:
        process_write_exception(LOG_FILE,url,'nssFailure')
        return "nssFailure" # if nssFailure
    elif 'e=dnsNotFound' in e.msg:
        process_write_exception(LOG_FILE,url,'DNS not found')
        return "dnsNotFound" # if DNS Not Found error
    elif 'e=redirectLoop' in e.msg:
        process_write_exception(LOG_FILE, url, 'Redirect Loop')
        return "redirect" # if redirect loop
    elif 'e=connectionFailure' in e.msg:
        process_write_exception(LOG_FILE,url,'Connection Failed')
        return "connexionfailure" # if connection failed
    else:
        print(f'Error capturing screenshot for {url}: {str(e.msg)}')
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f'Error: {url}\n')
        return "misc" # return if misc error
        
# todo: write tests for process_write_exception        
def process_write_exception(LOG_FILE,url,er): # function to process outputting exceptions - removes 12 lines of redundant code
    print(f'Error capturing screenshot for {url}: {er}')
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f'{er}: {url}\n')
    return 0
    
def driver(argv): #MAIN DRIVER FUNCTION
    # set CSV_FILE_PATH using process_default_args to check for valid CSV argument
    CSV_FILE_PATH = process_default_args(argv) # process arguments
    display_logo() #output the logo
    # configure options and initialisations
    options = Options()
    options.headless = True  # Run Firefox in headless mode (no GUI)
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options) #removed executable_path=GECKODRIVER_PATH as per selenium 4.6.0
    http,https,timeout,misc = 0,0,0,0 # initialise counters
    PAGE_LOAD_TIMEOUT = 10 # Set the maximum time to wait for a page to load (in seconds)

    # create directory for screenshots
    dir_name = build_dir_name()
    make_dir(dir_name)

    # File to log unreachable sites
    LOG_FILE = dir_name + '/unreachable_sites.txt'  # this will need to be built to prepend the dir name rather than test

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
            filename = dir_name + "/" + filename # prepend screenshot directory name here to save files in the correct directory
            try:
                # Load the webpage with a maximum timeout
                driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
                driver.get(url)
                # Take a screenshot
                driver.save_screenshot(filename)
                print(f'Screenshot saved for {url}')
                https += 1 # increment when success
            # if an exception occurs, try replacing https with http
            except Exception as e:
                #print(type(e))
                try: # try with http, screenshot and report success if successful
                    url = url.replace("https://", "http://")
                    driver.get(url)
                    driver.save_screenshot(filename)
                    print(f'Screenshot saved for {url}')
                    http += 1 # increment when successful
                # if page times out, report and log the exception
                except TimeoutException as e: # if page fails to load, process exception and increment timeout
                    process_std_exceptions(LOG_FILE, e, url, True) # pass in the optional param for timeout
                    timeout += 1 # increment if timeout
                except Exception as e:
                    misc += 1 # increment if miscellaneous exception
                    process_std_exceptions(LOG_FILE, e, url)
    # Quit the driver
    driver.quit()

    print("Execution completed successfully!")
    print_report(http,https,timeout,misc,extendReport) #print out the exit report

if __name__ == "__main__":
    driver(argv)
