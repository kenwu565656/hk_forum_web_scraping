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
import re

from Comment import Comment
from Post import Post

if __name__ == "__main__":

    posts = []
    possible_post_to_scrap = []

    driver = webdriver.Chrome()
    driver.get('https://forum.hkgolden.com/channel/HT')

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    arts = soup.find_all('div', {"class": ["jss272"]})
    authors = soup.find_all('summary', {"class": ["jss289"]})
    categorys = soup.find_all('div', {"class": ["jss264", "jss265"]})
    urls = soup.find_all('a', {"class": ["jss284"]})

    if len(arts) == 0:
        arts = soup.find_all('div', {"class": ["jss236"]})
        authors = soup.find_all('summary', {"class": ["jss253"]})
        categorys = soup.find_all('div', {"class": ["jss228", "jss229"]})
        urls = soup.find_all('a', {"class": ["jss248"]})

    possible_post_to_scrap.append(len(arts))
    possible_post_to_scrap.append(len(authors))
    possible_post_to_scrap.append(len(categorys))
    possible_post_to_scrap.append(len(urls))

    print(soup.prettify())

    for i in range(min(possible_post_to_scrap)):
        url = 'https://forum.hkgolden.com' + urls[i].attrs['href']
        topic = arts[i].getText()
        category = categorys[i].getText()
        post = Post(url, topic, category)

        post.set_PostID(post.url[post.url.find("thread/") + 7:])
        print(str(post))
        posts.append(post)

        break

    driver.close()

    for i in posts:

        # print(str(i))

        driver = webdriver.Chrome()
        driver.get(i.url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # contents = soup.find_all('meta')
        # contents = soup.find_all('div', {"class": ["jss279", "jss307"]})

        replys = soup.find_all('div', {"data-role": "reply"})
        print(replys)
        for reply in replys:
            comment_object = Comment(i.PostID)

            author = reply.find('span', {'class': ["MuiButton-label"]}).getText()

            comment_floor = reply.attrs['data-id']
            comment_object.setCommentFloor(comment_floor)

            info_div = reply.find_all('div')[0]
            author = info_div.find('div').find_all('div')[1].find('span').getText()

            time_div = info_div.find('div').find_all('div')[1].find_all('div')[1]
            time = time_div.find_all('span')[1].attrs['title']
            comment_object.setCommentDate(time)

            contentee_div = reply.find_all('div')[1]
            contentee = contentee_div.find('span').getText()
            comment_object.setCommenterName(contentee)

            content_div = reply.find_all('div')[6]
            comment_object.setCommentText(content_div.getText())

            quote = content_div.find('blockquote')
            if quote is not None:
                while quote.find('blockquote') is not None:
                    comment_object.setReply(quote.getText())

            print(comment_object)


        break

