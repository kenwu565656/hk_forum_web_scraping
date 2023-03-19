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
from Comment import Comment
from webScraperDAO import webScraperDAO

if __name__ == "__main__":

    posts = []
    possible_post_to_scrap = []
    dao = webScraperDAO()
    dao.setCursor()

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get('https://www.discuss.com.hk/hottopics.php')

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # print(soup.prettify())

    # discuss.com have 47 different category
    for i in range(47):

        hotTopic = soup.find('div', {"id": f"hottopics_{i}"})

        try:
            catoergory = hotTopic.find('div', {"class": "ht_sect"})

            arts = hotTopic.find_all('a')

            for art in arts:
                if art.attrs['href'] != "#index":
                    post = Post(f"https://www.discuss.com.hk/{art.attrs['href']}", art.getText(), catoergory.getText())

                    # Post id
                    postID_start_index = art.attrs['href'].find("tid=") + 4
                    postID_end_index = art.attrs['href'].find("&")
                    postID = art.attrs['href'][postID_start_index:postID_end_index]
                    post.set_PostID(postID)

                    posts.append(post)

        except AttributeError:
            print("Cannot load Catoergory")

    for post in posts:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(post.url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        content = soup.find("div", {"class": ["postmessage"]}).getText("", True)
        post.setPostText(content)

        author = soup.find('a', {"class": ["name", "line-clamp", "line-clamp-1"]})
        post.setPosterName(author.getText())
        authorID = author.attrs['href']
        authorID_start_index = authorID.find("uid=") + 4
        authorID = authorID[authorID_start_index:]
        post.set_PosterID(authorID)

        post_date = soup.find("div", {"class": ["post-date"]}).getText()
        # example of split ['#1', '發表於', '2023-3-4', '14:08']
        post.set_PostDate(":".join(post_date.split()[2:]))

        like = soup.find('button', {"class": ["like", " "]})
        like_number = like.attrs['data-value']
        post.setTotalLike(like_number)

        dislike = soup.find('button', {"class": ["dislike", " "]})
        dislike_number = dislike.attrs['data-value']
        post.setTotalUnlike(dislike_number)

        id = soup.find("div", {"class": ["fix-pid-landing"]}).attrs['id'][3:]
        post.setID(id)

        print(post)

        dao.insertPost("discusspost", post)
        time.sleep(1)

        # count how many page in a post
        pages_bar = soup.find('div', {"class": "pagination-buttons"})
        pages = pages_bar.find_all('a')
        max_page = 1
        for i in pages:
            max_page = max(max_page, int(i.attrs['data-pn']))
        print(max_page)
        driver.close()

        for page in range(1, int(max_page) + 1):
            print(f"We are in page {page}")
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get(f"{post.url}&extra=&page={page}")

            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            if page == 1:
                comments = soup.find_all("div", {"class": ["mainbox", "viewthread"]})[1:]
            else:
                comments = soup.find_all("div", {"class": ["mainbox", "viewthread"]})

            print(f"Page {page} have {len(comments)} comments")
            for comment in comments:

                comment_object = Comment(post.PostID)

                comment_author = comment.find('a', {"class": ["name", "line-clamp", "line-clamp-1"]})
                comment_object.setCommenterName(comment_author.getText())
                commenterID = comment_author.attrs['href']
                commenterID_start_index = commenterID.find("uid=") + 4
                commenterID = commenterID[commenterID_start_index:]
                comment_object.setCommenterID(commenterID)

                id = comment.find("div", {"class": ["fix-pid-landing"]}).attrs['id'][3:]
                comment_object.setID(id)

                comment_date = comment.find("div", {"class": ["post-date"]}).getText()
                # example of split ['#1', '發表於', '2023-3-4', '14:08']
                comment_object.setCommentDate(":".join(post_date.split()[2:]))

                commentFloor = comment.find("div", {"class": ["post-number"]}).getText("", True)
                # remove #, eg #14 -> 14
                comment_object.setCommentFloor(commentFloor[1:])

                quote = comment.find("blockquote")
                comment_content = comment.find("div", {"class": ["postmessage"]}).getText("", True)
                if quote is None:
                    comment_object.setReplyToID(post.PosterID)
                    comment_object.setReplyToName(post.PosterName)
                    comment_object.setReply(post.ID)
                else:
                    reply_to_name = quote.find("i").getText()
                    comment_object.setReplyToName(reply_to_name)
                    quoteText = quote.getText("", True).strip()
                    comment_content = comment_content[(comment_content.find(quoteText) + len(quoteText)):]
                    replyID = quote.find("a").attrs["href"]
                    replyID = replyID[replyID.find("&pid") + 4: replyID.find("&ptid")]
                    comment_object.setReply(replyID)
                comment_object.setCommentText(comment_content)

                like = comment.find('button', {"class": ["like", " "]})
                like_number = like.attrs['data-value']
                comment_object.setTotalLike(like_number)

                dislike = comment.find('button', {"class": ["dislike", " "]})
                dislike_number = dislike.attrs['data-value']
                comment_object.setTotalUnlike(dislike_number)

                print(comment_object)
                dao.insertComment("discusscomment", comment_object)
                time.sleep(1)

            driver.close()



