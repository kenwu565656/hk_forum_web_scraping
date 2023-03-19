import mysql.connector
from datetime import datetime
import json
from uuid import uuid4
import uuid
class webScraperDAO:
      def __init__(self):
          connection_file = open('connection.json')
          connection_detail = json.loads(connection_file)
          print(connection_detail)
          self.db = mysql.connector.connect(host=connection_detail["host"],
                                            user=connection_detail["user"],
                                            password=connection_detail["password"],
                                            port=connection_detail["port"],
                                            database=connection_detail["database"])
          self.cursor = self.db.cursor()

      def getCursor(self):
          mycursor = self.db.cursor()
          return mycursor

      def setCursor(self):
          self.cursor = self.db.cursor()

      def insertPost(self, table, post):
          sql = f"INSERT INTO {table} (Url, Topic, SocialMediaSource," \
                f"PostID, PosterID, PostDate," \
                f"PosterName, PostText, ID," \
                f"TotalLike, TotalUnlike, TotalLove," \
                f"TotalHaha, TotalYay, TotalWow," \
                f"TotalSad, TotalAngry, createdtime)" \
                f" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
          timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          val = (post.url, post.topic, post.socialMediaSource,
                 post.PostID, post.PosterID, post.PostDate,
                 post.PosterName, str(post.PostText), timestamp
                 , post.TotalLike, post.TotalUnlike, post.TotalLove,
                 post.TotalHaha, post.TotalYay, post.TotalWow,
                 post.TotalSad, post.TotalAngry, timestamp)

          try:
            self.cursor.execute(sql, val)
            self.db.commit()
          except:
            print('insert fail')
            self.db.rollback()

      def insertComment(self, table, comment):
          sql = f"INSERT INTO {table} (PostID, CommenterID, CommentDate," \
                f"CommenterName, commentText, replyToName," \
                f"replyToID, commentFloor, ID," \
                f"TotalLike, TotalUnlike, TotalLove," \
                f"TotalHaha, TotalYay, TotalWow," \
                f"TotalSad, TotalAngry, createdtime, Reply)" \
                f" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
          timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          val = (comment.postId, comment.commenterID, comment.commentDate,
                 comment.commenterName, str(comment.commentText), comment.replyToName,
                  comment.replyToID, comment.commentFloor, timestamp
                 , comment.TotalLike, comment.TotalUnLike, comment.TotalLove,
                 comment.TotalHaha, comment.TotalYay, comment.TotalWow,
                 comment.TotalSad, comment.TotalAngry, timestamp, comment.reply)

          try:
              self.cursor.execute(sql, val)
              self.db.commit()
              print('inserted')
          except Exception as e:
              print('insert fail')
              print(e)
              self.db.rollback()








