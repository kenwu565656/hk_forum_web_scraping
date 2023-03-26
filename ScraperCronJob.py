from apscheduler.schedulers.background import BackgroundScheduler
from Handler.ScraperHandlers import scraperHandler

class CronJob():
    def __init__(self, forum):
        self.scheduler = BackgroundScheduler()
        self.forum = forum
        self.scheduler.add_job(self.job, 'interval', minutes=1440)

    def job(self):
        scraperHandler(self.forum)

    def start(self):
        self.scheduler.start()



