from bs4 import *
from config import *
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def driver_init():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    service = Service(executable_path=DRIVER)
    driver = webdriver.Chrome(options=chrome_options,service=service)
    return driver

def scrape(topic):
    driver = driver_init()
    driver.get(URL)
    time.sleep(5)
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(topic)
    button_box = driver.find_element(By.ID,"gs_hdr_tsb")
    button_box.click()

    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"gs_res_ccl_mid")))

    content = driver.page_source

    soup = BeautifulSoup(content,"html.parser")
    topics = []
    papers = soup.find_elements(By.CLASS_NAME,"gs_r gs_or gs_scl")
    print(papers)
    
    for paper in papers:
        Title = paper.find_element(By.ID,"JTvu6eNE3PwJ").text
        Link =  paper.find_element(By.ID,"JTvu6eNE3PwJ").get_attribute("href")
        elements = paper.find_element(By.CLASS_NAME, "gs_a")
        elems = elements.text.split('-')
        Author_Attr = elems[0]
        if len(Author_Attr.split(',')) == 1:
            Author = Author_Attr
        else:
            Author = Author_Attr.split(',')[0]
        Year_Attr = elems[1]
        if len(Year_Attr.split(',')) == 2:
            Year = Year_Attr.split(',')[1]
        else:
            Year = Year_Attr
        params = paper.find_element(By.CLASS_NAME,"gs_fl gs_flb")
        links = params.find_elements(By.NAME,'a')
        for  link in links:
            if link.text.startswith('Cited'):
                Cite = link.text.split()
                Cited = Cite[2]
        Research = {
            "Title": Title,
            "Author": Author,
            "Year": Year,
            "Cite": Cited,
            "Link" : Link
        }


        topics.append(Research)

    driver.quit()

    return topics

            
print(scrape("Inroduction to Computing"))