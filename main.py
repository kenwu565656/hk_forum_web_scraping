from flask import Flask
from config import DevConfig
from Handler.ScraperHandlers import scraperHandler
from ScraperCronJob import CronJob

app = Flask(__name__)
app.config.from_object(DevConfig)

lihkgScraperCronJob = CronJob("lihkg")
lihkgScraperCronJob.start()

goldenScraperCronJob = CronJob("golden")
goldenScraperCronJob.start()

BabyDiscussScraperCronJob = CronJob("BabyDiscuss")
BabyDiscussScraperCronJob.start()

BabyKingdomScraperCronJob = CronJob("BabyKingdom")
BabyKingdomScraperCronJob.start()

@app.route('/scraper/<string:forum>')
def index(forum):
    scraperHandler(forum)

if __name__ == '__main__':
    app.run()



