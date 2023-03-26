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

from Models.Comment import Comment
from Models.Post import Post
from Repository.webScraperDAO import webScraperDAO
from interface.scraper import Scraper


class BabyKingdomScraper(Scraper):

    def __init__(self):
        self.posts_list = []
        self.possible_post_to_scrap = []
        self.dao = webScraperDAO()
        self.dao.setCursor()
        self.pattern = re.compile(r'^(normalthread_)')

    def getPosts(self, source):
        for page in range(1):

            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            # driver.maximize_window()
            driver.get(f'https://www.baby-kingdom.com/forum.php?mod=forumdisplay&fid=162&page={page}')

            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.close()

            posts = soup.find_all('tbody', {"id": [self.pattern]})

            for post in posts:
                post_header = post.find('td', {"class": ["new"]}).find('a')

                url = "https://www.baby-kingdom.com/" + post_header.attrs['href']
                topic = post_header.getText()
                post_object = Post(url, topic, "162")
                post_object.set_PostID(post.attrs["id"][13:])

                post_time_and_author = post.find('td', {"class": ["by", "by_author"]})
                author_link = post_time_and_author.find('a')
                author = author_link.getText()
                author_id = author_link.attrs["href"][author_link.attrs["href"].find("uid=") + 4:]
                post_time = post_time_and_author.find('em').getText()

                post_object.set_PosterID(author_id)
                post_object.setPosterName(author)
                post_object.set_PostDate(post_time)
                self.posts_list.append(post_object)

                self.dao.insertPost("babykingdompost", post_object)
                time.sleep(1)
                print(str(post_object))
                break



    def getCommentsInPosts(self, postUrl):
        for post in self.posts_list:
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            # driver.maximize_window()
            driver.get(post.url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.close()

            pages_bar = soup.find('div', {"class": ["btn-group", "pagination-select"]})
            pages = pages_bar.find('button').getText()
            pages = pages[pages.find("/ ") + 2:]

            for page in range(1, int(pages)):
                driver = webdriver.Chrome()
                driver.maximize_window()
                driver.get(post.url + f"&page={str(page)}")
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                floors = soup.find_all('div', {"class": "postthread"})
                driver.close()



                for floor in floors:
                    comment_object = Comment(post.PostID)

                    comment_id = floor.attrs['id'][3:]
                    comment_object.setID(comment_id)

                    comment_info = floor.find('div', {'class': "p_info"})
                    if comment_info is not None:
                        comment_link = comment_info.find('div', {'class': ["pi", "username"]}).find('a')
                        commenterID = comment_link.attrs['href']
                        commenterID = commenterID[commenterID.find("&uid=") + 5:]
                        commenterName = comment_link.getText()
                        comment_object.setCommenterName(commenterName)
                        comment_object.setCommenterID(commenterID)

                    comment_content = floor.find('div', {'class': "p_content"})
                    print(comment_content.getText())
                    if comment_content is not None:
                        try:
                            comment_floor = comment_content.find('div', {'class': ['pi']})
                            comment_floor = comment_floor.find('em').getText()
                            print(comment_floor)
                            comment_object.setCommentFloor(comment_floor)

                            comment_time = comment_content.find('div', {'class': ['pti']}).find('span').attrs['title']
                            print(comment_time)
                            comment_object.setCommentDate(comment_time)
                            print(comment_object)

                            comment_text = comment_content.find('span', {"id": [re.compile(r'^(postmessage_)')]})
                            if comment_text is None:
                                comment_text = comment_content.find('div', {"id": [re.compile(r'^(postmessage_)')]})
                            comment_object.setCommentText(comment_text.getText(), True)
                        except:
                            print("cannot find comment content")
                            continue

                    comment_quote = floor.find('blockquote')
                    if comment_quote is not None:
                        comment_to = comment_quote.find('font', {'color': ['#999999']}).getText()
                        comment_to = comment_to[: comment_to.find(' ')]
                        comment_object.setReplyToName(comment_to)

                        reply = comment_quote.find('a').attrs['href']
                        reply_start_index = reply.find('&pid') + 4
                        reply_end_index = reply.find('&ptid')
                        reply = reply[reply_start_index:reply_end_index]
                        comment_object.setReply(reply)

                    print(comment_object)
                    self.dao.insertComment("babykingdomcomment", comment_object)
                    time.sleep(1)



