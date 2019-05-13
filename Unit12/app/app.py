from flask import Flask, render_template, url_for,flash, jsonify, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

app = Flask(__name__)

app.config.from_object('config')
mongo = PyMongo(app)

db_collection = mongo.db.get_collection(app.config.get('MARS_COLLECTION_NAME'))

@app.route('/')
def home():
    mars_doc = db_collection.find_one({'_id' : app.config.get('MARS_DOCUMENT_ID')})

    if mars_doc:
        return render_template('index.html',mars_document=mars_doc['content'])
    else:
        return render_template('index.html',mars_document=None)

@app.route('/scrape')
def run_scrape():

    scrape_document = {'_id' : app.config.get('MARS_DOCUMENT_ID'), 'content' : scrape()}

    if db_collection.find_one({'_id' : app.config.get('MARS_DOCUMENT_ID')}):
        db_collection.replace_one({'_id' : app.config.get('MARS_DOCUMENT_ID')}, scrape_document)

    else:
        db_collection.insert_one(scrape_document)

    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(port=5000, debug=True)    
