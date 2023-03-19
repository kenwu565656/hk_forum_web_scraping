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
from webScraperDAO import webScraperDAO
dao = webScraperDAO()
dao.setCursor()

if __name__ == "__main__":

    posts = []
    possible_post_to_scrap = []

    driver = webdriver.Chrome()
    driver.get('https://lihkg.com/category/2')

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    arts = soup.find_all('div', {"class": ["wQ4Ran7ySbKd8PdMeHZZR"]})
    print(len(arts))
    for art in arts:

        author = art.find('span', {'class': ["CxY4XDSSItTeLVg0cKCN0", "A0jheqYUBHNW93KykXKEH"]})

        like = art.find_all('span', {'class': ["_37XwjAqVHtjzqzEtybpHrU"]})[1]

        number_of_page = art.find('div', {'class': ["_26oEXjfUS_iHzbxYcZE6bD"]})

        url = art.find('a', {'class': ["_2A_7bGY9QAXcGu1neEYDJB"]}).attrs['href']
        url = url[:url.find('/page')]

        category = art.find('a', {'class': ["_3VRxq3mC-jm2fhdX4exwPU"]})
        if category is not None:
            category = category.getText()

        topic = art.find('span', {'class': ["_20jopXBFHNQ9FUbcGHLcHH"]})
        if topic is not None:
            topic = topic.getText()

        post = Post("https://lihkg.com" + url, topic, category)

        post.setPosterName(author.getText())
        post.setTotalLike(like.getText("", True))

        post.page = number_of_page.getText("", True)
        post.page = post.page[:post.page.find(" ")]

        post_id = url[url.find('thread/') + 7:]
        post.set_PostID(post_id)

        print(post.page)
        posts.append(post)
        print(post)

        dao.insertPost("lihkgpost", post)
        time.sleep(1)


    driver.close()

    for post in posts:
        for page in range(int(post.page)):
            driver = webdriver.Chrome()
            driver.get(f'{post.url}/page/{page}')

            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            replys = soup.find_all('div', {'class': ["_2bokd4pLvU5_-Lc97NVqzn", "rBpBkc4uTvfskasqoALQM", "_20q6NML4ErQq8usNV-npj5"]})

            for reply in replys:
                comment_object = Comment(post.PostID)

                reply_floor = reply.attrs['id']
                comment_object.setCommentFloor(reply_floor)

                commentID = reply.attrs['data-post-id']
                comment_object.setID(commentID)

                info = reply.find('small', {'class': ["_1VcuFUmnOEK51TsshmrnJM"]})
                commenterInfo = info.find('a')
                commenterName = commenterInfo.getText()
                comment_object.setCommenterName(commenterName)
                commenterID = commenterInfo.attrs['href'][9:]
                comment_object.setCommenterID(commenterID)

                comment_time = info.find('span', {'class': ["Ahi80YgykKo22njTSCzs_"]})
                comment_time = comment_time.attrs['title']
                comment_object.setCommentDate(comment_time)

                content_div = reply.find('div', {'class': ["GAagiRXJU88Nul1M7Ai0H"]})
                content = content_div.find('div', {'class': ["_2cNsJna0_hV8tdMj3X6_gJ"]})
                comment_object.setCommentText(content)

                like = reply.find_all('label', {'class': ["_1yxPOd27pAzF9olhItRDej", "_2iRKJuMIV77zdwLRreUgLK"]})[0]
                dislike = reply.find_all('label', {'class': ["_1yxPOd27pAzF9olhItRDej", "_2iRKJuMIV77zdwLRreUgLK"]})[1]
                comment_object.setTotalLike(like.getText())
                comment_object.setTotalUnlike(dislike.getText())

                quote = reply.find('blockquote')
                if quote is not None:
                    comment_object.setReply(quote)

                print(comment_object)
                dao.insertComment("lihkgcomment", comment_object)
                time.sleep(1)





