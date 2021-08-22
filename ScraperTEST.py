import time
import shutil
import glob
import os
import csv
from dotenv import load_dotenv

import pandas as pd
import time

from selenium import webdriver
from bs4 import BeautifulSoup
from tabulate import tabulate

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

## NOTE: Manually set Chrome browser to download PDFs instead of opening them

# IMPROVEMENTS TO MAKE:
# Set browser to save pdfs as a file instead of opening in the browser window
# Replace the time.sleep(3) calls to something that waits for the page to load
# before executing a command
# https://stackoverflow.com/questions/59130200/selenium-wait-until-element-is-present-visible-and-interactable

# Change the working directory to the dir where this and the mergePDFs files are
os.chdir('/Users/christianbeaudrie/PythonProjects/PDFScraper/')
currentPath = os.getcwd()

## TSBC Incident Summaries
filePath = '/Users/christianbeaudrie/downloads/TSBC_Incidents'
filenameBase = 'TSBC'
URL = 'https://www.technicalsafetybc.ca/state-safety/incident-investigations'

chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "plugins.always_open_pdf_externally": True,
    "download.default_directory": filePath,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.plugins_disabled": ["Chrome PDF Viewer"]
    }
)

browser = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)

nextPageAvailable = True

count = 0
browser.get(URL)

while nextPageAvailable:
     # Get element for next page
    next = browser.find_elements_by_class_name("pager__item--next")
   
    




    ## Decide whether to loop again or quit
    t = len(next) # if length is 0, no link for the next page
    count = count + 1

    # If there is a URL for the next page, grab it and loop, else, quit
    if t > 0:
        for element in next:
            lnks=element.find_elements_by_tag_name("a")
            for lnk in lnks:
                nextURL = lnk.get_attribute("href") # Get hrefs

        print("Count: " + str(count))
        print("Navigating to: " + nextURL)
        browser.get(nextURL)
    
    else:
        print("=== FINISHED ===")
        nextPageAvailable = False


    



