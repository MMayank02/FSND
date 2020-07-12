# Capstone Book Store

The application is live on Heroku. There are 4 methods exposed as listed below

# GET Method (GET /books , /books-details)


    url = "https://uda-capstone.herokuapp.com/books-details"  --> No Auth needed
    url = "https://uda-capstone.herokuapp.com/books-details"  --> Needs staff or owner Auth


# POST Method (POST /books)

    url = "https://uda-capstone.herokuapp.com/books"

    json request body

                {
                "bookname" : "mock",
                "author" : "mocker",
                "price" : 10,
                "category" : "play",
                "quantity" :100,
                "agegroup" : "0-3"
            }

# Patch method (PATCH /books/<id>)
    url = "https://uda-capstone.herokuapp.com/books/<id>"

    json request body
    
             {
                "category" : "play",
                "quantity" :100,
                "agegroup" : "0-3"
            }

# Delete method (DELETE /books/<id>)
    url = "https://uda-capstone.herokuapp.com/books/<id>"

# ROLES

End Points are secured by Auth0 JWT token validation. There are 2 roles defined

    1) Staff - Permissions (get:books, patch:books)

    Bearer - eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjExLW1uM3NIQ2taSHJDX0J0LXFmNyJ9.eyJpc3MiOiJodHRwczovL2Rldi00MzUwYWlqZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwYjIyOWMyZWIzMDMwMDE5Yzg2NjczIiwiYXVkIjoiYm9va3Nob3AiLCJpYXQiOjE1OTQ1NjU0OTEsImV4cCI6MTU5NDYzNzQ5MSwiYXpwIjoiRUZneGxxdFM5dDFVdDdSbmhucVR5bHRwZjNDdjRuT0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpib29rcyIsInBhdGNoOmJvb2tzIl19.kk3qCREfz1WIABeTYPN_hTHHpMX1YYVYX85fdlBELk9M9tqHS_yCDDpIy71TIgjmT0W5MhcoCyeGkJ92VOFUmPB63xxW2t1e5mcrSmbh7aXecTSrCWGJe8M6ynLS0tXnS6CZHbB4l_IndcPRrGmajUFkPtSRyfIc0NScPZiI2OmJ-yhnjxbScv4tEBePMv-UNO1GnnhGRdCXtFZiLFXtZ3QLsrBC1HsQSYNNCIt-t8n001QC_DrRDAokUj2t0F-q1TxxPIB_5oOORpVUmoCSg673xhbySw7kD7jdDz69EXlmORczcbRoahPUg8QQlQwbGgvw1tGzswj9uvBa7AUiCw

    Token validity till - Juy 13, 16:21:31 GMT

    2) Owner - Permissions (get:books, post:books, patch:books, delete:books)

    Bearer - eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjExLW1uM3NIQ2taSHJDX0J0LXFmNyJ9.eyJpc3MiOiJodHRwczovL2Rldi00MzUwYWlqZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwOWZmOWYyZWIzMDMwMDE5Yzg2MmU2IiwiYXVkIjoiYm9va3Nob3AiLCJpYXQiOjE1OTQ1NjQ4ODUsImV4cCI6MTU5NDYzNjg4NSwiYXpwIjoiRUZneGxxdFM5dDFVdDdSbmhucVR5bHRwZjNDdjRuT0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpib29rcyIsImdldDpib29rcyIsInBhdGNoOmJvb2tzIiwicG9zdDpib29rcyJdfQ.HYA5k1NJsX2K-v4VQxV1o07ofnRKdW85TFVbRyR0E0Q2ElG4h6XoTWt1YUva_n0bGNRPMcZeuDnHdT0dyiiBzOFyCTWr26G-0JqLClcd8xRr61KlNm_ph6XUeWB_6vpsO4LReB_0YjwDS8AXe-x8m5HzRuL7zG5012rnbD77bbZ8Q-8jlVpd-hFSwSxYFEGBhIB63uwpTHL6U3O3Tt6-IzwuBchbUcgTfrnY18MOryghXZj9BUzTn_qNWt0Rt7S6Shscz5kjd7Et_4Qe3rpTxrp6Quics9_C2KM7qRhBOOB9c004lkXA-JskXWC7NCIAPy_4d05eSg2KmhPUZwFWZQ

    Token validity till - Juy 13, 16:21:31 GMT

    RBAC access has been defined. The new token can be generated via

    https://dev-4350aijg.us.auth0.com/authorize?audience=bookshop&response_type=token&client_id=EFgxlqtS9t1Ut7RnhnqTyltpf3Cv4nOG&redirect_uri=http://localhost:8100/capslogin-results

## Running application locally
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/kidszone` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- CORS for Cross Origin reference

- Migrations for DB

- psycopg2 for DB driver

## Running the server

From within the `./kidszone` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### API reference

The backend API is available at below endpoints when run locally

Backend Base URL: http://127.0.0.1:5000/

## API Respomse
GET '/books' 
{
    "books": [
        {
            "age_id": 1,
            "category_id": 3,
            "id": 2,
            "quantity": 5
        },
        {
            "age_id": 1,
            "category_id": 2,
            "id": 3,
            "quantity": 5
        }
    ],
    "success": true
}

GET /books-detail 
{
    "books": [
        {
            "agegrp": "9-12",
            "author": "neha",
            "bookname": "blogger",
            "category": "science",
            "price": 10,
            "quantity": 100
        },
        {
            "agegrp": "9-12",
            "author": "neha",
            "bookname": "blogger",
            "category": "science",
            "price": 10,
            "quantity": 100
        },
        {
            "agegrp": "0-3",
            "author": "mocker",
            "bookname": "mock",
            "category": "play",
            "price": 10,
            "quantity": 100
        }
    ],
    "success": true
}

POST /books

{
    "message": "Book created successfully!",
    "success": true
}

PATCH /books/<id>
{
    "book": [
        {
            "age_id": 4,
            "category_id": 1,
            "id": 4,
            "quantity": 100
        }
    ],
    "message": "Book updated successfully!",
    "success": true
}

DELETE /books/<id>
{
    "delete": 1,
    "success": true
}

```
Errors are returned in the following json format:

      {
        "success": "False",
        "error": <error code>,
        "message": "<error message>",
      }
The error codes currently returned are:

400 – bad request error
401 - Token expired., Incorrect claims. 
401 - Please check the audience and issuer.
403 - Unable to parse authentication token. 
403 - Unable to find the appropriate key.
404 – resource not found
422 – Unprocessable
500 – An error has occured, please try again

### TESTING

    1) From within the `./kidszone` directory run python3 test_capstone.py to execute the Unit Test cases

    2) Also postman collection with bearer token is setup for use and is available within kidszone folder. To run it export the collection udacity-fsnd-capston.json to postman and execute.

## Sourcecode

    The sourcecode will be available for forking at MMayank02/FSND/projects/capstone/kidszone
