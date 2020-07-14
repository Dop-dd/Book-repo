import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 


app = Flask(__name__)
# add mongodb name and the uri
app.config["MONGO_DBNAME"] = 'library_books'
app.config["MONGO_URI"] = "mongodb+srv://root:rOOtUser@myfirstcluster.ilffs.mongodb.net/library_books?retryWrites=true&w=majority"

# create an instance of py_mongo with app as argument
mongo = PyMongo(app)


# define the various menu options
@app.route('/')
@app.route('/get_books')
def get_books():
    return render_template('books.html', books=mongo.db.books.find())


@app.route('/')
@app.route('/get_media')
def get_media():
    return render_template('media.html', media=mongo.db.media.find())


@app.route('/add_book')
def add_book():
    return render_template('add_book.html',
                           faculties=mongo.db.faculties.find())


@app.route('/add_media')
def add_media():
    return render_template('add_media.html',
                           media=mongo.db.media.find())


# Add submit button for media
@app.route('/insert_media', methods=['POST'])
def insert_media():
    media = mongo.db.media
    media.insert_one(request.form.to_dict())
    return redirect(url_for('get_books'))


# Add submit button for Books
@app.route('/insert_book', methods=['POST'])
def insert_book():
    book = mongo.db.books
    book.insert_one(request.form.to_dict())
    return redirect(url_for('get_books'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)