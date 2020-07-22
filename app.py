import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 


app = Flask(__name__)
# add mongodb name and the uri
app.config["MONGO_DBNAME"] = 'library_books'
app.config["MONGO_URI"] = "mongodb+srv://root:rOOtUser@myfirstcluster.ilffs.mongodb.net/library_books?retryWrites=true&w=majority"

# create an instance of py_mongo with app as argument
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')


# define the various menu options
@app.route('/get_books')
def get_books():
    return render_template('books.html', books=mongo.db.books.find())


# Add a book
@app.route('/add_book')
def add_book():
    return render_template('add_book.html',
                           faculties=mongo.db.faculties.find())


# Add submit button for Books
@app.route('/insert_book', methods=['POST'])
def insert_book():
    book = mongo.db.books
    book.insert_one(request.form.to_dict())
    return redirect(url_for('get_books'))


# wire the edit button
@app.route('/edit_book/<book_id>')
# description task, name, due date, is urgent fields will be
# pre-populated based on the information returned in the task.
def edit_book(book_id):
    a_book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    # category names will be prepolulated based on the collection
    # # of categories returned in the categories cursor
    all_faculties = mongo.db.faculties.find()
    return render_template('edit_book.html',
                           book=a_book, faculties=all_faculties)


@app.route('/update_book/<book_id>', methods=['POST'])
def update_book(book_id):
    # access the database collection
    book = mongo.db.books
    # call the update function, specify an id
    book.update({'_id': ObjectId(book_id)},
    {
        'faculty_name': request.form.get('faculty_name'),
        'subject_name': request.form.get('subject_name'),
        'book_title': request.form.get('book_title'),
        'book_author': request.form.get('book_author'),
        'book_description': request.form.get('task_description'),
        'lender_name': request.form.get('lender_name'),
        'due_date': request.form.get('due_date'),
        'is_available': request.form.get('is_urgent')
    })
    return redirect(url_for('get_books'))
# specify the form fields to match the keys on the task collection


# delete a book
@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    mongo.db.books.remove({'_id': ObjectId(book_id)})
    return redirect(url_for('get_books'))


# find a book by Id
@app.route('/find_book/<book_title>/', methods=['GET'])
def find_book(book_title):
    book = mongo.db.books.find_one({'_id': ObjectId(book_title)},
    {
        'book_title': request.form.get('book_title'),
    })
    return render_template('find.html', book=book)


# find a book by using a search field
@app.route('/get_one/', methods=['GET'])
def get_one():
    book_title = mongo.db.books
    book = mongo.db.books.find_one({'book_title': ''})
    print(book_title)
    return render_template('get_one.html',
                           book=book, book_title=book_title)


# categories function
@app.route('/get_faculties')
def get_faculties():
    return render_template('faculties.html',
                           faculties=mongo.db.faculties.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)