from flask import Flask
from config import DevConfig
from ScraperCronJob import CronJob
from apscheduler.schedulers.background import BackgroundScheduler

def running():
    print("Cron Job is running")

app = Flask(__name__)
app.config.from_object(DevConfig)

scheduler = BackgroundScheduler()

scheduler.add_job(running, 'interval', seconds=20)
scheduler.start()

lihkgScraperCronJob = CronJob("lihkg")
lihkgScraperCronJob.start()

goldenScraperCronJob = CronJob("golden")
goldenScraperCronJob.start()

BabyDiscussScraperCronJob = CronJob("BabyDiscuss")
BabyDiscussScraperCronJob.start()

BabyKingdomScraperCronJob = CronJob("BabyKingdom")
BabyKingdomScraperCronJob.start()

if __name__ == '__main__':
    app.run(port=5001)