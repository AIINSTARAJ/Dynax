from bs4 import *
from .config import *
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

'''def driver_init():
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
    return driver'''

def scrape(topic):
    formatted_topic = topic.replace(" ", "+")
    url = f"https://scholar.google.com/scholar?q={formatted_topic}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url,headers=headers)

    time.sleep(0)

    soup = BeautifulSoup(response.text,"html.parser")
    papers = soup.find_all("div", class_ = "gs_ri")
    topics = []
    for paper in papers:
        Title_A = paper.find("h3",class_ = "gs_rt")
        Title = Title_A.text.upper()
        Link_A = Title_A.find('a')
        Link = Link_A.get('href')
        elements = paper.find("div", class_ = "gs_a").text
        elems = elements.split('-')
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
        params = paper.find("div",class_ = "gs_fl gs_flb")
        links = params.find_all('a')
        for  link in links:
            if link.text.startswith('Cited'):
                Cite = link.text.split(" ")
                Cited = Cite[2]
        Research = {
            "Title": Title,
            "Author": Author,
            "Year": Year,
            "Cite": Cited,
            "Link" : Link
        }


        topics.append(Research)

    return topics
