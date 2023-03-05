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
    driver.get('https://www.babydiscuss.com/top?period=daily')

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    arts = soup.find_all('a', {"class": ["title", "raw-link", "raw-top-link"]})
    channel = soup.find_all('span', {"class": "category-name"})
    number = soup.find_all('button', {"class": ["btn-link", "posts-map", "badge-posts", "heatmap-low"]})
    view = soup.find_all('td', {"class": ["num", "views", "topic-list-data"]})
    date = soup.find_all('span', {"class": "relative-date"})

    possible_post_to_scrap.append(len(arts))
    possible_post_to_scrap.append(len(channel))
    possible_post_to_scrap.append(len(number))
    possible_post_to_scrap.append(len(view))
    possible_post_to_scrap.append(len(date))

    for i in range(min(possible_post_to_scrap)):
        url = arts[i].attrs['href']
        topic = arts[i].getText()
        category = channel[i].getText()
        post = Post(url, topic, category)

        #number_of_comment = number[i].find('span', {"class": "number"}).getText()
        #views = view[i].find('span', {"class": "views"}).getText()
        #last_comment_date = date[i].getText().strip()

        posts.append(post)

    driver.close()
    for i in posts:

        # print(str(i))

        driver = webdriver.Chrome()
        driver.get(i.url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', {"class": ["cooked"]})
        i.setContent(content)
        # print(content.getText())

        comments = soup.find_all('div', {"class": "row"})
        print(len(comments))
        for comment in comments:
            commentee = comment.find('span', {"class": ["first", "username"]}).find('a').getText()

            print(comment.getText())
            # print(commentee)
            commentContent = comment.find('div', {"class": ["cooked"]}).getText()
            # print(commentContent)
            try:
                numberOfLike = comment.find('button', {"class": ["like-count"]}).getText()
            except:
                numberOfLike = 0
            # print(numberOfLike)
        break

