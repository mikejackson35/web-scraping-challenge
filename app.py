from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars_data)


@app.route("/scrape")
def scrape():
    scraped_data = scrape_mars.scrape()
    mongo.db.mars.update({}, {"$set": scraped_data}, upsert=True)
    mongo.db.update_one({}, {"$set": scraped_data}, upsert=True)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)