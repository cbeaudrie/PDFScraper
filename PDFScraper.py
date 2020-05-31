import time
import shutil
import glob
import os
from dotenv import load_dotenv
 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

## NOTE: Manually set Chrome browser to download PDFs instead of opening them

# IMPROVEMENTS TO MAKE:
# Set browser to save pdfs as a file instead of opening in the browser window
# Replace the time.sleep(3) calls to something that waits for the page to load
# before executing a command
# https://stackoverflow.com/questions/59130200/selenium-wait-until-element-is-present-visible-and-interactable

# Change the working directory to the dir where this and the mergePDFs files are
os.chdir('/Users/christianbeaudrie/PythonProjects/PDFScraper/')
currentPath = os.getcwd()

year = 2020
issueIndex = 1 # 0 means latest issue in the year

# ## Stanford Social Innovation Review
# filePath = '/Users/christianbeaudrie/downloads/Stanford'
# filenameBase = 'Stanford'
# URL = 'https://gw2jh3xr2c.search.serialssolutions.com/log?L=GW2JH3XR2C&D=AKVCP&J=STANSOCINR&P=Link&PT=EZProxy&H=23709d71e9&U=https%3A%2F%2Fezproxy.library.ubc.ca%2Flogin%3Furl%3Dhttps%3A%2F%2Fsearch.ebscohost.com%2Fdirect.asp%3Fdb%3Dbsu%26jid%3DW5W%26scope%3Dsite'

# ## Harvard Business Review
# filePath = '/Users/christianbeaudrie/downloads/HBR'
# filenameBase = 'HBR'
# URL = 'https://ezproxy.library.ubc.ca/login?url=https://search.ebscohost.com/direct.asp?db=bsu&jid=HBR&scope=site'

## MIT Technology Review
filePath = '/Users/christianbeaudrie/downloads/MIT'
filenameBase = 'MIT'
URL = 'https://gw2jh3xr2c.search.serialssolutions.com/log?L=GW2JH3XR2C&D=EAP&J=MITTECREV&P=Link&PT=EZProxy&H=af42e1068a&U=https%3A%2F%2Fezproxy.library.ubc.ca%2Flogin%3Furl%3Dhttps%3A%2F%2Fsearch.ebscohost.com%2Fdirect.asp%3Fdb%3Daph%26jid%3D2M1%26scope%3Dsite'

# Launch browser and open URL
browser = webdriver.Chrome()
browser.get(URL)

# Grab reference to the current window in case getPDFs errors out. Can switch back to this window if needed
current_window = browser.current_window_handle 

# Open CWL Login Page and log in
cwlButton = browser.find_element_by_xpath("//a[@role = 'button']")
cwlButton.click()

# Get element ids for the login form
loginElem = browser.find_element_by_id('username')
passwordElem = browser.find_element_by_id('password')

# Get username and password from .env
load_dotenv(currentPath + '/.env')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Fill the form and submit
loginElem.send_keys(USERNAME)
passwordElem.send_keys(PASSWORD)

loginButton = browser.find_element_by_name('_eventId_proceed')
loginButton.click()

# Pause until 2FA is completed
input("Complete login with Two Factor Authentication. Press Enter when ready ...")

# Open up the year folder
selectYear = browser.find_element_by_link_text('+ ' + str(year))
selectYear.click()

# Get links to all issues:
allIssues = browser.find_elements_by_class_name('authVolIssue_issue_cell')

# Get the latest issue
# Get the child of the selected element which is clickable
selectedIssue = allIssues[issueIndex].find_element_by_xpath("./*") 
selectedIssueName = selectedIssue.text
selectedIssue.click()

# Download pdfs on the page
# https://stackoverflow.com/questions/43488737/force-page-to-open-in-new-window-selenium-web-driver-python

pdfLinks = browser.find_elements_by_link_text('PDF Full Text')  

from getPDFs import getPDFs
getPDFs(browser, pdfLinks)

## Once finished, move everything into a folder
filesGlob = glob.glob('/Users/christianbeaudrie/downloads/ContentServer*.pdf')

selectedIssueName = selectedIssueName.replace('/', ' to ')

newFilePath = filePath + ' ' + selectedIssueName

if not os.path.exists(newFilePath):
    os.makedirs(newFilePath)

for file in filesGlob:
    shutil.move(file, newFilePath)

## Call mergePDFs

fullFilename = filenameBase + '_' + selectedIssueName

from mergePDFs import mergePDFs
mergePDFs( newFilePath, fullFilename, True )


