class Comment:
    def __init__(self, postId):
        self.postId = postId
        self.commentText = None
        self.commenterID = None
        self.commenterName = None
        self.replyToName = None
        self.replyToID = None
        self.commentFloor = None
        self.commentDate = None
        self.commentee = None
        self.TotalLike = None
        self.TotalUnLike = None
        self.TotalLove = None
        self.TotalHaha = None
        self.TotalYay = None
        self.TotalWow = None
        self.TotalSad = None
        self.TotalAngry = None

    def setCommentText(self, commentText):
        self.commentText = commentText

    def setCommenterID(self, commenterID):
        self.commenterID = commenterID

    def setCommenterName(self, commenterName):
        self.commenterName = commenterName

    def setReplyToName(self, replyToName):
        self.replyToName = replyToName

    def setReplyToID(self, replyToID):
        self.replyToID = replyToID

    def setCommentFloor(self, commentFloor):
        self.commentFloor = commentFloor

    def setCommentDate(self, commentDate):
        self.commentDate = commentDate

    def setCommentee(self, commentee):
        self.commentee = commentee

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
        return f'Post ID = {self.postId}\n' \
               f'commentText = {self.commentText}\n' \
               f'commenterID = {self.commenterID}\n' \
               f'commenterName = {self.commenterName}\n' \
               f'reply to name = {self.replyToName}\n' \
               f'commentFloor = {self.commentFloor}\n' \
               f'commentDate = {self.commentDate}\n' \
               f'reply to id = {self.replyToID}\n' \
               f'TotalLike = {self.TotalLike}\n' \
               f'TotalUnLike = {self.TotalUnLike}\n' \
               f'TotalLove = {self.TotalLove}\n' \
               f'TotalHaha = {self.TotalHaha}\n' \
               f'TotalYay = {self.TotalYay}\n' \
               f'TotalWow = {self.TotalWow}\n' \
               f'TotalSad = {self.TotalSad}\n' \
               f'TotalAngry = {self.TotalAngry}\n'



