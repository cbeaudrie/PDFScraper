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


# FUNCTION ------------------
def follow_links(pageURL):
    print('IN follow_links')
    browser.get(pageURL)
    pdfElements = browser.find_elements_by_class_name("file--application-pdf")

    print(pdfElements)

    for element in pdfElements:
        aTag=element.find_elements_by_tag_name("a")
        pdfLink = aTag[0].get_attribute("href")
        pdfFilename = aTag[0].text
        aTag[0].click()

    print("PDF DETAILS:")
    print(pdfLink)
    print(pdfFilename)

    return [pdfFilename, pdfLink]
# ------------------------------


# FUNCTION ------------
def get_table_rows():
    html=browser.page_source
    soup=BeautifulSoup(html,'html.parser')
    table_data=soup.select_one("table")
    return table_data
# ---------------------



# FUNCTION ------------------


# ---------------------------


# NEXT THING TO DO
# ONCE FINISHED GETTING PDFS AT ALL OF THE LINKS, THEN ON THE MAIN PAGE CLICK ON THE '> NEXT ' BUTTON
# TO GO TO THE NEXT PAGE AND REPEAT THE PROCESS. CONTINUE UNTIL THERE IS NO '>NEXT' BUTTON AVAILABLE (IS THE END)



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

nextPageAvailable = True
firstPass = True

table_headers = []
table_names = []

count = 0

browser = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
browser.get(URL)

while nextPageAvailable:
     # Get element for next page (before navigating away)
    next = browser.find_elements_by_class_name("pager__item--next")
   
    

    ## Get table rows
    table_data = get_table_rows()

    ## Create dataframe (alternative approach)
    # table=pd.read_html(str(table_data))
    # print(table[0])

    ## Scrape table data

    # Scrape data from the table

    links = []

    if firstPass:
        for header in table_data.find_all("thead"):
            for th in header.find_all("th"):
                table_headers.append(th.text)
            table_headers.insert(1, "Summary Link")
            table_headers.insert(5, "Technology Link")
            table_headers.append("PDF Name")
            table_headers.append("PDF Link")
        firstPass = False

    for body in table_data.find_all("tbody"): 
        # for field_title in body.find_all(class_="views-field-title"):
        #     for link in field_title.find_all("a", href=True):
        #         links.append(link['href'])
        for tr in body.find_all("tr"):
            td_names = []
            for td in tr.find_all("td"):
                td_names.append(td.text)
                for link in td.find_all("a", href=True):
                    td_names.append("https://www.technicalsafetybc.ca" + link['href'])
            table_names.append(td_names)

    print("********LINKS***********")
    print(links)

    # Get links to all of the summary pages
    summaryPageLinks = []

    titleCells = browser.find_elements_by_class_name("views-field-title")  # Get elements with hrefs

    for cell in titleCells:
        lnks=cell.find_elements_by_tag_name("a")
        for lnk in lnks:
            summaryPageLinks.append(lnk.get_attribute("href")) # Get hrefs

    summaryPageLinks.pop(0) # remove the first URL
    # print(summaryPageLinks)
    # print("*******")
    # print(summaryPageLinks)
    # print("*******")

    summaryPageLinks_TEST = summaryPageLinks[0:1]
    print(summaryPageLinks_TEST)

    ## Open each link - save PDF info and download PDFs
    pdfDetailsList = []
    i=1

    for page in summaryPageLinks_TEST:
        print(i, ' of ', len(summaryPageLinks), ' downloading...')
        print("----------")
        print(page)
        details = follow_links(page)
        # print("DETAILS")
        # print(details)
        pdfDetailsList.append(details)
        # print(i, ' DONE')
        i=i+1

    # print("PDFDETAILSLIST")
    # print(pdfDetailsList)
    # print("Length pdfDetailsList")
    # print(len(pdfDetailsList))
    # print("length table_names")
    # print(len(table_names))

    # PREPARE TO PRINT TO CSV
    j=0
    for row in table_names:
        if j < len(pdfDetailsList):
            row.append(pdfDetailsList[j][0])
            row.append(pdfDetailsList[j][1])
        j=j+1
    
    # print("*** ROW ***")
    # print(row)


# next = browser.find_elements_by_class_name("pager__item--next")
# print(next.text)
# next[0].click()

# --------------------------








    ## ----------- Decide whether to loop again or quit
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



    ## Write to file
    with open('TSBC_table_new.csv', 'w') as f:
        
        # using csv.writer method from CSV package
        write = csv.writer(f)
        
        write.writerow(table_headers)
        write.writerows(table_names)








while nextPageAvailable:

    browser.get(URL)

    next = browser.find_elements_by_class_name("pager__item--next")
    print("NEXT")
    print(next)

    # Grab reference to the current window in case getPDFs errors out. Can switch back to this window if needed
    current_window = browser.current_window_handle 

#     ## Get table rows
#     table_data = get_table_rows()

#     ## Create dataframe (alternative approach)
#     # table=pd.read_html(str(table_data))
#     # print(table[0])

#     ## Scrape table data

#     # Scrape data from the table

#     links = []

#     if firstPass:
#         for header in table_data.find_all("thead"):
#             for th in header.find_all("th"):
#                 table_headers.append(th.text)
#             table_headers.insert(1, "Summary Link")
#             table_headers.insert(5, "Technology Link")
#             table_headers.append("PDF Name")
#             table_headers.append("PDF Link")
#         firstPass = False

#     for body in table_data.find_all("tbody"): 
#         # for field_title in body.find_all(class_="views-field-title"):
#         #     for link in field_title.find_all("a", href=True):
#         #         links.append(link['href'])
#         for tr in body.find_all("tr"):
#             td_names = []
#             for td in tr.find_all("td"):
#                 td_names.append(td.text)
#                 for link in td.find_all("a", href=True):
#                     td_names.append("https://www.technicalsafetybc.ca" + link['href'])
#             table_names.append(td_names)

#     print("********LINKS***********")
#     print(links)

#     # Get links to all of the summary pages
#     summaryPageLinks = []

#     titleCells = browser.find_elements_by_class_name("views-field-title")  # Get elements with hrefs

#     for cell in titleCells:
#         lnks=cell.find_elements_by_tag_name("a")
#         for lnk in lnks:
#             summaryPageLinks.append(lnk.get_attribute("href")) # Get hrefs

#     summaryPageLinks.pop(0) # remove the first URL
#     # print(summaryPageLinks)
#     # print("*******")
#     # print(summaryPageLinks)
#     # print("*******")

#     summaryPageLinks_TEST = summaryPageLinks[0:1]
#     print(summaryPageLinks_TEST)

#     ## Open each link - save PDF info and download PDFs
#     pdfDetailsList = []
#     i=1

#     for page in summaryPageLinks_TEST:
#         print(i, ' of ', len(summaryPageLinks), ' downloading...')
#         print("----------")
#         print(page)
#         details = follow_links(page)
#         # print("DETAILS")
#         # print(details)
#         pdfDetailsList.append(details)
#         # print(i, ' DONE')
#         i=i+1

#     # print("PDFDETAILSLIST")
#     # print(pdfDetailsList)
#     # print("Length pdfDetailsList")
#     # print(len(pdfDetailsList))
#     # print("length table_names")
#     # print(len(table_names))

#     # PREPARE TO PRINT TO CSV
#     j=0
#     for row in table_names:
#         if j < len(pdfDetailsList):
#             row.append(pdfDetailsList[j][0])
#             row.append(pdfDetailsList[j][1])
#         j=j+1
    
#     # print("*** ROW ***")
#     # print(row)


# # next = browser.find_elements_by_class_name("pager__item--next")
# # print(next.text)
# # next[0].click()

# # --------------------------

# ## Write to file
# with open('TSBC_table_new.csv', 'w') as f:
      
#     # using csv.writer method from CSV package
#     write = csv.writer(f)
      
#     write.writerow(table_headers)
#     write.writerows(table_names)
