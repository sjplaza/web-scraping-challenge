from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_nasa

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/nasa_app"
mongo = PyMongo(app)


@app.route("/")
def home():
    mars_info = mongo.db.collection.find_one()
    return render_template("index.html", mars="mars_info")


@app.route("/scrape")
def scrape():
    listings = mongo.db.collection.update({}, mars_data, upsert=True)
    mars_data = scrape_mars.scrape()
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
