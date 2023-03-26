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


class BabyDiscussScraper(Scraper):

    def __init__(self):
        self.posts = []
        self.possible_post_to_scrap = []
        self.dao = webScraperDAO()
        self.dao.setCursor()

    def getPosts(self, source):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.babydiscuss.com/top?period=daily')
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()

        arts = soup.find_all('a', {"class": ["title", "raw-link", "raw-top-link"]})
        channel = soup.find_all('span', {"class": "category-name"})
        number = soup.find_all('button', {"class": ["btn-link", "posts-map", "badge-posts", "heatmap-low"]})
        view = soup.find_all('td', {"class": ["num", "views", "topic-list-data"]})
        date = soup.find_all('span', {"class": "relative-date"})

        self.possible_post_to_scrap.append(len(arts))
        self.possible_post_to_scrap.append(len(channel))
        self.possible_post_to_scrap.append(len(number))
        self.possible_post_to_scrap.append(len(view))
        self.possible_post_to_scrap.append(len(date))

        for i in range(min(self.possible_post_to_scrap)):
            url = arts[i].attrs['href']
            topic = arts[i].getText()
            category = channel[i].getText()
            post = Post(url, topic, category)

            PostID_index = url.find("/topic/")
            PostID = url[PostID_index + 7:]
            post.set_PostID(PostID)
            self.posts.append(post)

    def getCommentsInPosts(self, postUrl):
        for i in self.posts:

            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(i.url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.close()

            try:
                content = soup.find('div', {"class": ["cooked"]}).getText()
                i.setPostText(content)
            except:
                print("cannot find post Context")

            try:
                postTime = soup.find('span', {"class": ["relative-date"]}).attrs["data-time"]
                i.set_PostDate(postTime)
            except:
                print("cannot find post date")

            try:
                article = soup.find("article", {"class": ["boxed", "onscreen-post"]})
                i.setID(article.attrs["data-post-id"])
            except:
                print("cannot find post id")

            try:
                poster = article.find('span', {"class": ["first", "username"]}).find('a')
                i.setPosterName(poster.getText())
                i.set_PosterID(poster.attrs["href"][3:])
            except:
                print("cannot find poster name")

            try:
                numberOfLike = article.find('button', {"class": ["like-count"]}).getText()
            except:
                numberOfLike = 0
            i.setTotalLike(numberOfLike)

            print(i)

            self.dao.insertPost("babydiscusspost", i)
            time.sleep(1)

            comments = soup.find_all('article', {"class": ["boxed", "onscreen-post"]})
            print(len(comments))

            for comment in comments:

                comment_object = Comment(i.PostID)

                try:
                    commentee = comment.find('span', {"class": ["first", "username"]}).find('a').getText()
                    comment_object.setCommenterName(commentee)
                except:
                    print("cannot find commentee")

                try:
                    commentContent = comment.find('div', {"class": ["cooked"]}).getText("", True)
                    comment_object.setCommentText(commentContent)
                except:
                    print("cannot find comment Text")

                try:
                    numberOfLike = comment.find('button', {"class": ["like-count"]}).getText()
                except:
                    numberOfLike = 0
                comment_object.setTotalLike(numberOfLike)

                try:
                    quote = comment.find('aside', {"class": ["quote", "no-group"]})
                    replyToName = quote.attrs["data-username"]

                    blackquote = quote.find('blockquote')
                    reply = blackquote.attrs["id"]
                    reply_text = blackquote.getText()
                    commentContent = commentContent[commentContent.find(reply_text) + len(reply_text):]

                    comment_object.setReplyToName(replyToName)
                    comment_object.setReply(reply)
                    comment_object.setCommentText(commentContent)

                except:
                    print("no quote")


                # find comment id
                try:
                    comment_id = comment.attrs["data-post-id"]
                    comment_object.setID(comment_id)
                except:
                    print("cannot find comment_id")

                # find comment_floor
                try:
                    comment_floor = comment.attrs["id"][5:]
                    comment_object.setCommentFloor(comment_floor)
                except:
                    print("cannot find comment floor")

                # find comment date
                try:
                    postTime = comment.find('span', {"class": ["relative-date"]}).attrs["data-time"]
                    comment_object.setCommentDate(postTime)
                except:
                    print("cannot find post time")

                print(comment_object)

                self.dao.insertComment("badydiscusscomment", comment_object)
                time.sleep(1)

