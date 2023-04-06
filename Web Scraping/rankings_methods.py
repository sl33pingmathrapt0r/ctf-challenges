from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs

def scrape_rankings_list(driver: webdriver.Chrome, url_main: str, page: int) -> list:
    """
    Used for a list of data entries presented over 
    multiple pages in a c-table. 

    Given an (incomplete) URL link with the current 
    page number, parse through the entire list across
    all pages and return the data. 
    
    (PS. current definition of function is specific to 
    YesWeHack rankings page)
    """
    url= url_main + str(page)
    driver.get(url)

    # explicitly wait for table elements to load, 
    # since table loaded dynamically
    wait = WebDriverWait(driver, 180)
    table= wait.until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
    assert table, "table not loaded"
    
    content= driver.page_source
    entries= []
    
    soup= bs(content)
    header= soup.find('thead').find('tr')
    
    for row in soup.find_all('tr'):
        if row==header: continue
        
        hunter= row.find('td', attrs={'class': 'hunter'}).getText()
        rank= row.find('td', attrs={'class': 'rank'}).getText()
        point= row.find('td', attrs={'class': 'u-text-center points'}).getText()
        public= row.find('a', attrs={'class':'o-flex'})
        profile_url= '-' if not public else public.get('href')
        
        entries.append({})
        entries[-1]['hunter']= hunter
        entries[-1]['rank']= int(rank[:-2])
        entries[-1]['point']= int(point.replace(',', ''))
        entries[-1]['url']= profile_url
        entries[-1]['public']= bool(public)
    
    if soup.find('ywh-icon', attrs= {'icon': 'arrow-right'}):
        return entries+ scrape_rankings_list(driver, url_main, page+1)
        
    return entries
        


# trial method
"""
Using Selenium and Beautiful Soup, obtain from the 
page source, elements that are relevant. Clean the data
and store appropriately.  
"""

# URL_MAIN= 'https://yeswehack.com/'
# YEARS= range(2016, 2024)

# chrome driver added to PATH
# driver= webdriver.Chrome('chromedriver')
# driver.minimize_window()
# url_tag= 'ranking?period=All&page='
# hunters= tools.scrape_rankings_list(driver, URL_MAIN+url_tag, 1)