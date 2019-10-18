from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_data

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars" 
mongo = PyMongo(app)

@app.route("/test")
def test():
  return "Hello, World!"

@app.route("/")
def home():
  mars_mission = mongo.db.mars_mission.find_one()
  return render_template("index.html", mars_data=mars_mission)

@app.route("/scrape")
def scrape():
  mars_mission = mongo.db.mars_mission
  mars_data = scrape_data()
  mars_mission.update({}, mars_data, upsert=True)
  return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
