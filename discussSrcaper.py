from bs4 import BeautifulSoup
import requests
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
from Post import Post

if __name__ == "__main__":

    posts = []
    possible_post_to_scrap = []

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://www.discuss.com.hk/hottopics.php')

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # print(soup.prettify())

    for i in range(47):

        hotTopic = soup.find('div', {"id": f"hottopics_{i}"})

        try:
            catoergory = hotTopic.find('div', {"class": "ht_sect"})

            arts = hotTopic.find_all('a')

            for art in arts:
                if art.attrs['href'] != "#index":
                    post = Post(f"https://www.discuss.com.hk/{art.attrs['href']}", art.getText(), catoergory.getText())
                    posts.append(post)

        except AttributeError:
            print("Cannot load Catoergory")

    for post in posts:
        print(str(post))
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(post.url)

        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        content = soup.find_all("div", {"class": ["postmessage"]})[0].getText()
        post.setPostText(content)

        author = soup.find('a', {"class": ["name", "line-clamp", "line-clamp-1"]})
        post.setPosterName(author)

        pages_bar = soup.find('div', {"class": "pagination-buttons"})
        pages = pages_bar.find_all('a')
        max_page = 1
        for i in pages:
            max_page = max(max_page, int(i.attrs['data-pn']))
        print(max_page)
        driver.close()
        for page in range(1, int(max_page) + 1):
            print(page)
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get(f"{post.url}&extra=&page={page}")

            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            if page == 1:
                comments = soup.find_all("div", {"class": ["mainbox", "viewthread"]})[1:]
            else:
                comments = soup.find_all("div", {"class": ["mainbox", "viewthread"]})
            print(len(comments))
            for comment in comments:

                comment_content = comment.find("div", {"class": ["postmessage"]}).getText()
                print(comment_content.strip())

                comment_author = comment.find('a', {"class": ["name", "line-clamp", "line-clamp-1"]})
                print(comment_author.getText())
            driver.close()
        break

