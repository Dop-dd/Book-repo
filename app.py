import os
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import pymongo

app = Flask(__name__)
# add mongodb name and the uri
app.config["MONGO_DBNAME"] = 'books'
app.config["MONGO_URI"] = "mongodb+srv://root:rOOtUser@myfirstcluster.ilffs.mongodb.net/books?retryWrites=true&w=majority"

# create an instance of py_mongo with app as argument
mongo = PyMongo(app)


# define the various menu options
@app.route('/')
@app.route('iget_books')
def get_books():
    return render_template('books.html', tasks=)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)