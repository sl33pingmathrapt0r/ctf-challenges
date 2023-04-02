from selenium import webdriver
import rankings_methods as tools

import pandas as pd
import json

URL_MAIN= 'https://yeswehack.com/'
YEARS= range(2016, 2024)

# METHOD 1
"""
Using Selenium and Beautiful Soup, obtain from the 
page source, elements that are relevant. Clean the data
and store appropriately.  
"""

# chrome driver added to PATH
# driver= webdriver.Chrome('chromedriver')
# driver.minimize_window()
# url_tag= 'ranking?period=All&page='
# hunters= tools.scrape_rankings_list(driver, URL_MAIN+url_tag, 1)


# METHOD 2 
"""
Having determined that the table is dynamically loaded, 
the webpage must be retrieving the data from some file 
over the network. Looking at the files sent over the 
network when loading the page reveals JSON files. 
Retrieve the JSON files. 
"""

page= 0
all_url= 'https://api.yeswehack.com/ranking?page='
periodic_url= 'https://api.yeswehack.com/ranking/2022/M12?page='