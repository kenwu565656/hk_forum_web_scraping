class Post:
    def __init__(self, url, topic, category):
        self.url = url
        self.topic = topic
        self.socialMediaSource = category
        self.ID = None
        self.PostID = None
        self.PosterID = None
        self.PostDate = None
        self.PosterName = None
        self.PostText = None
        self.TotalLike = None
        self.TotalUnLike = None
        self.TotalLove = None
        self.TotalHaha = None
        self.TotalYay = None
        self.TotalWow = None
        self.TotalSad = None
        self.TotalAngry = None

    def set_url(self, url):
        self.url = url

    def set_topic(self, topic):
        self.topic = topic

    def set_socialMediaSource(self, socialMediaSource):
        self.socialMediaSource = socialMediaSource

    def setID(self, ID):
        self.ID = ID

    def set_PostID(self, PostID):
        self.PostID = PostID

    def set_PosterID(self,PosterID):
        self.PosterID = PosterID

    def set_PostDate(self, PostDate):
        self.PostDate = PostDate

    def setPosterName(self, PosterName):
        self.PosterName = PosterName

    def setPostText(self, PostText):
        self.PostText = PostText

    def setTotalLike(self, TotalLike):
        self.TotalLike = TotalLike

    def setTotalUnlike(self, TotalUnLike):
        self.TotalUnLike = TotalUnLike

    def setTotalLove(self, TotalLove):
        self.TotalLove = TotalLove

    def setTotalHaha(self, TotalHaha):
        self.TotalHaha = TotalHaha

    def setTotalYay(self, TotalYay):
        self.TotalYay = TotalYay

    def setTotalWow(self, TotalWow):
        self.TotalWow = TotalWow

    def setTotalSad(self, TotalSad):
        self.TotalSad = TotalSad

    def setTotalAngry(self, TotalAngry):
        self.TotalAngry = TotalAngry

    def __str__(self):
        return f'Post url = {self.url}\n' \
               f'Topic = {self.topic}\n' \
               f'Category = {self.socialMediaSource}\n' \
               f'ID = {self.ID}\n' \
               f'PostID = {self.PostID}\n' \
               f'PosterID = {self.PosterID}\n' \
               f'PostDate = {self.PostDate}\n' \
               f'PosterName = {self.PosterName}\n' \
               f'PostText = {self.PostText}\n' \
               f'TotalLike = {self.TotalLike}\n' \
               f'TotalUnLike = {self.TotalUnLike}\n' \
               f'TotalLove = {self.TotalLove}\n' \
               f'TotalHaha = {self.TotalHaha}\n' \
               f'TotalYay = {self.TotalYay}\n' \
               f'TotalWow = {self.TotalWow}\n' \
               f'TotalSad = {self.TotalSad}\n' \
               f'TotalAngry = {self.TotalAngry}\n'