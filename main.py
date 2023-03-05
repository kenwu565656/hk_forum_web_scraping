from bs4 import BeautifulSoup
import requests
import pandas as pd

# URL = "https://forum.hkgolden.com/channel/HT"
# URL = "https://www.uwants.com"
# URL = "https://www.babydiscuss.com/top"
# html = requests.get(URL)
# soup = BeautifulSoup(html.text, "html.parser")

# print(soup)


import time
import os
import pandas as pd
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import date, timedelta, datetime
from urllib import parse, request
import json


def generate_date_list(start_year, start_month, start_day, end_year, end_month, end_day):
    time_list = []
    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)
    ranges = pd.date_range(start_date, end_date, freq='B')
    for i in ranges:
        time_list.append(str(i.date()))
    return time_list


def to_web():
    options = Options()
    options.add_experimental_option("prefs", {
        # "download.default_directory": current,
        "download.prompt_for_download": False
    })
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(r'https://forum.hkgolden.com/channel/HT')
    action = webdriver.ActionChains(driver)
    return driver, action


def enter_stock_name(stock_name):
    stock_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yfin-usr-qry"]')))
    stock_input.send_keys(stock_name)
    stock_input.send_keys(Keys.ENTER)
    historical_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="quote-nav"]/ul/li[5]/a')))
    historical_button.click()


def enter_time_range(start_day, start_month, start_year, end_day, end_month, end_year):
    path_of_time_key = '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/svg/path'
    time_key = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, path_of_time_key)))
    time_key.click()
    path_of_start_time = '//*[@id="dropdown-menu"]/div/div[1]/input'
    start_time_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, path_of_start_time)))
    start_time_input.send_keys(start_day)
    start_time_input.send_keys("TAB")
    start_time_input.send_keys(start_month)
    start_time_input.send_keys("TAB")
    start_time_input.send_keys(start_year)
    start_time_input.send_keys("TAB")
    action.send_keys(end_day)
    action.send_keys("TAB")
    action.send_keys(end_month)
    action.send_keys("TAB")
    action.send_keys(end_year)
    action.send_keys("TAB")
    action.send_keys("ENTER")
    action.perform()


def download():
    path_of_download_key = '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a'
    download_key = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, path_of_download_key)))
    download_key.click()


def rename_downloaded_file():
    while not os.listdir(current):
        time.sleep(1)
    last = max([os.path.join(current, f) for f in os.litdir(current)], key = os.path.getctime)
    shutil.move(last, os.path.join(current, stock + download_time))


def go():
    os.chdir(os.path.dirname(__file__))
    current = os.getcwd()
    try:
        os.makedirs(current + "Data_downloaded")
    except FileExistsError:
        # directory already exists
        pass
    current = current + "Data_downloaded"
    driver, action = to_web()
    stock = "AAPL"
    enter_stock_name(stock, driver)
    enter_time_range("01", "12", "2021", "12", "2", "2022", driver, action)
    download()
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    download_time = now.strftime("%d/%m/%Y %H:%M:%S")
    rename_downloaded_file()


if __name__ == "__main__":


    #driver, action = to_web()
    #time.sleep(10)
    #resp = requests.get("https://forum.hkgolden.com/channel/HT")
    #soup = BeautifulSoup(resp.text, 'html.parser')
    #arts = soup.find_all('div', class_='jss215')
    #print(arts)
    #for art in arts:
    #    title = art.find('summary', class_='jss220').getText().strip()
    #    print(title)
    # result = driver.find_elements(By.CLASS_NAME, "jss236")
    # print(result)
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup)


    driver = webdriver.Chrome()
    driver.get('https://www.babydiscuss.com/top')

    time.sleep(5)

    resp = requests.get('https://www.babydiscuss.com/top')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    arts = soup.find_all('td', {"class": ["main-link", "clearfix", "topic-list-data"]})
    number = soup.find_all('span', {"class": "number"})
    date = soup.find_all('span', {"class": "relative-date"})
    # print(resp.text)
    # print(arts)
    for i in range(10):
        print("title")
        print(arts[i].getText().split()[0].strip())
        print("channel")
        print(arts[i].getText().split()[1].strip())
        print("view")
        print(number[i].getText().strip())
        print("date")
        print(date[i].getText().strip())
        print("\n")

    driver = webdriver.Chrome()
    driver.get('https://forum.hkgolden.com/channel/HT')

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #arts = soup.find_all('a', {"class": "jss216"})
    number = soup.find_all('summary')
    date = soup.find_all("small", {"class": ""})
    # print(resp.text)
    for i in range(10):
        print("title")
        print(arts[i].getText().split()[0].strip())
        print("channel")
        print(arts[i].getText().split()[1].strip())
        print("view")
        print(number[i].getText().strip())
        print("date")
        print(date[i].getText().strip())
        print(date[i].extract(1))
        print("\n")



