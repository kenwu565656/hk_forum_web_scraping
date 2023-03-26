from flask import Flask
from config import DevConfig
from Handler.ScraperHandlers import scraperHandler

app = Flask(__name__)
app.config.from_object(DevConfig)


@app.route('/scraper/<string:forum>')
def index(forum):
    scraperHandler(forum)


if __name__ == '__main__':
    app.run()
