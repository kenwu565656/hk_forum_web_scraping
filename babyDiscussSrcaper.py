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

from Comment import Comment
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

        PostID_index = url.find("/topic/")
        PostID = url[PostID_index + 7:]
        post.set_PostID(PostID)

        posts.append(post)

    driver.close()
    for i in posts:

        driver = webdriver.Chrome()
        driver.get(i.url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', {"class": ["cooked"]}).getText()
        i.setPostText(content)

        postTime = soup.find('span', {"class": ["relative-date"]}).attrs["data-time"]
        i.set_PostDate(postTime)

        article = soup.find("article", {"class": ["boxed", "onscreen-post"]})
        i.setID(article.attrs["data-post-id"])

        poster = article.find('span', {"class": ["first", "username"]}).find('a')
        i.setPosterName(poster.getText())
        i.set_PosterID(poster.attrs["href"][3:])

        try:
            numberOfLike = article.find('button', {"class": ["like-count"]}).getText()
        except:
            numberOfLike = 0
        i.setTotalLike(numberOfLike)

        print(i)

        comments = soup.find_all('article', {"class": ["boxed", "onscreen-post"]})
        print(len(comments))

        for comment in comments:

            comment_object = Comment(i.PostID)

            commentee = comment.find('span', {"class": ["first", "username"]}).find('a').getText()
            comment_object.setCommenterName(commentee)

            commentContent = comment.find('div', {"class": ["cooked"]}).getText("", True)
            comment_object.setCommentText(commentContent)
            # print(commentContent)

            try:
                numberOfLike = comment.find('button', {"class": ["like-count"]}).getText()
            except:
                numberOfLike = 0

            try:
                quote = comment.find('aside', {"class": ["quote", "no-group"]})
                replyToName = quote.attrs["data-username"]

                blackquote = quote.find('blockquote')
                reply = blackquote.attrs["id"]
                reply_text = blackquote.getText()
                commentContent = commentContent[commentContent.find(reply_text) + len(reply_text): ]

                comment_object.setReplyToName(replyToName)
                comment_object.setReply(reply)
                comment_object.setCommentText(commentContent)

            except:
                print("no quote")
            comment_object.setTotalLike(numberOfLike)

            # find comment id
            comment_id = comment.attrs["data-post-id"]
            comment_object.setID(comment_id)

            # find comment_floor
            comment_floor = comment.attrs["id"][5:]
            comment_object.setCommentFloor(comment_floor)

            #find comment date
            postTime = comment.find('span', {"class": ["relative-date"]}).attrs["data-time"]
            comment_object.setCommentDate(postTime)

            print(comment_object)



        break

