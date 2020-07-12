import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random, json, logging
from flask_migrate import Migrate
from controllers.auth import AuthError, requires_auth
from database.models import setup_db, Books, Category, Kidsage

BOOKS_PER_PAGE = 5


# create and configure the app
app = Flask(__name__)
setup_db(app)
#migrate = Migrate(app,db)

'''
Function to paginate books 

'''


def paginated_books(request, books):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * BOOKS_PER_PAGE
    end = start + BOOKS_PER_PAGE
    finalbooks = []
    for book in books:
        finalbooks.append ({
                    "id" : book.id,
                    "quantity" : book.quantity,
                    "category_id" : book.category_id,
                    "age_id"  : book.age_id,
        })
    
    current_books = finalbooks[start:end]
    return current_books

'''
Function to paginate book details 

'''

def paginated_books_details(request, books):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * BOOKS_PER_PAGE
    end = start + BOOKS_PER_PAGE
    finalbookdetails = []
    for book in books:
        Category.id = book.category_id
        Kidsage.id = book.age_id
        category_ext = Category.query.get(Category.id)
        agegrp_ext = Kidsage.query.get(Kidsage.id)
        finalbookdetails.append ({
                    "bookname" : book.bookname,
                    "author" : book.author,
                    "price" : book.price,
                    "quantity" : book.quantity,
                    "category" : category_ext.type,
                    "agegrp"  : agegrp_ext.agegroup,
        })
    
    current_book_details = finalbookdetails[start:end]
    return current_book_details

'''
Endpoint to GET all books details 

'''
@app.route('/books')
def get_all_books():
    all_data = Books.query.order_by(Books.id).all()
    books_data = paginated_books(request, all_data)
    if (len(books_data) == 0):
        abort(404)
    return jsonify({
    'success': True,
    'books': books_data
    }), 200

'''
Endpoint to GET all books details 

'''
@app.route('/books-details')
@requires_auth('get:books')
def get_all_books_details(payload):
    all_data = Books.query.order_by(Books.id).all()
    books_data = paginated_books_details(request, all_data)
    if (len(books_data) == 0):
        abort(404)
    return jsonify({
    'success': True,
    'books': books_data
    }), 200

'''
Endpoint to delete book based on ID 

'''

@app.route('/books/<int:id>', methods=['DELETE'])
@requires_auth('delete:books')
def delete_book(payload, id):
    book = Books.query.filter(Books.id == id).one_or_none()

    if not book:
        abort(404)

    try:
        book.delete()
    except BaseException:
        abort(400)

    return jsonify({'success': True, 'delete': id}), 200

'''
Endpoint to post books 

'''

@app.route('/books', methods=['POST'])
@requires_auth('post:books')
def insert_book(payload):
    data = request.get_json()
    ibookname = data.get('bookname','')
    iauthor = data.get('author','')
    iprice = data.get('price', '')
    iquantity = data.get('quantity', '')
    icategory = data.get('category', '')
    iagegroup = data.get('agegroup','')

    

    if ((ibookname == '') or (iauthor == '') or (icategory == '')
            or (iprice == '') or (iquantity == '')) or (iagegroup == ''):
        abort(422)

    
    ctgrid = Category.query.filter(Category.type == icategory).one_or_none()
    agrpid = Kidsage.query.filter(Kidsage.agegroup == iagegroup).one_or_none()
    if ((ctgrid is None) or (agrpid is None)):
        abort(422)

    try:
        book = Books(
                    bookname = ibookname,
                    author = iauthor,
                    price  = iprice,
                    quantity  = iquantity,
                    category_id  = ctgrid.id,
                    age_id  = agrpid.id
                    )
        book.insert()

        # return success message
        return jsonify({
                    'success': True,
                    'message': 'Book created successfully!'
        }), 200

    except Exception:
        abort(500)

'''
Endpoint to update books quantity, type, agegroup 

'''

@app.route('/books/<int:id>', methods=['PATCH'])
@requires_auth('patch:books')
def update_book(payload, id):
    req = request.get_json()
    book = Books.query.filter(Books.id == id).one_or_none()

    if not book:
        abort(404)

    try:
        req_quantity = req.get('quantity','')
        req_category_id = req.get('category_id','')
        req_age_id = req.get('age_id','')

        if req_quantity:
            book.quantity = req_quantity

        if (req_category_id != ''):
            book.category_id = req_category_id

        if (req_age_id != ''):
            book.age_id = req_age_id

        book.update()
        
        updbook = Books.query.filter(Books.id == id)
        bookjson = paginated_books(request, updbook)

    except BaseException:
        abort(400)

    return jsonify({'success': True, 'book': bookjson, 'message': 'Book updated successfully!'}), 200

## Error Handling
'''
error handlers using the @app.errorhandler(error) decorator

'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

# Error handler for resource not found (400)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request error'
    }), 400

# Error handler for resource not found (404)
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404

# Error handler for internal server error (500)
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'An error has occured, please try again'
    }), 500

'''
Error handler for AuthError
 
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

if __name__ == '__main__':
    app.run()