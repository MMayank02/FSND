import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from controllers.auth import AuthError, requires_auth
from database.models import setup_db, Books, Category, Kidsage


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "testcaps"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.headers = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjExLW1uM3NIQ2taSHJDX0J0LXFmNyJ9.eyJpc3MiOiJodHRwczovL2Rldi00MzUwYWlqZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwOWZmOWYyZWIzMDMwMDE5Yzg2MmU2IiwiYXVkIjoiYm9va3Nob3AiLCJpYXQiOjE1OTQ1NjQ4ODUsImV4cCI6MTU5NDYzNjg4NSwiYXpwIjoiRUZneGxxdFM5dDFVdDdSbmhucVR5bHRwZjNDdjRuT0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpib29rcyIsImdldDpib29rcyIsInBhdGNoOmJvb2tzIiwicG9zdDpib29rcyJdfQ.HYA5k1NJsX2K-v4VQxV1o07ofnRKdW85TFVbRyR0E0Q2ElG4h6XoTWt1YUva_n0bGNRPMcZeuDnHdT0dyiiBzOFyCTWr26G-0JqLClcd8xRr61KlNm_ph6XUeWB_6vpsO4LReB_0YjwDS8AXe-x8m5HzRuL7zG5012rnbD77bbZ8Q-8jlVpd-hFSwSxYFEGBhIB63uwpTHL6U3O3Tt6-IzwuBchbUcgTfrnY18MOryghXZj9BUzTn_qNWt0Rt7S6Shscz5kjd7Et_4Qe3rpTxrp6Quics9_C2KM7qRhBOOB9c004lkXA-JskXWC7NCIAPy_4d05eSg2KmhPUZwFWZQ'
            }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
     Test for each test for successful operation and for expected errors.
    """

    def test_get_all_books(self):
        """Test books"""

        response = self.client().get('/books')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_all_books_details(self):
        """Test books details"""

        response = self.client().get('/books-details', headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_create_books(self):
        """Test for creating book."""
        mock_data = {
                "bookname" : "Mockname",
                "author" : "mock",
                "price" : 10,
                "category" : "sport",
                "quantity" :8,
                "agegroup" : "9-12"
            }
        response = self.client().post('/books', json=mock_data, headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))

        # asserions to ensure successful request
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Book created successfully!')

    def test_invalid_books_page(self):
        """Test for invalid Page"""
        response = self.client().get('/books?page=100')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_autheader_booksdet_error(self):
        """Test for Authorisation failure"""
        response = self.client().get('/books-details?page=100')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

        
    def test_delete_books_with_invalid_id(self):
        """Tests deletion of books with invalid id"""
        # this tests an invalid id
        response = self.client().delete('/books/abc12346', headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    def test_create_book_with_empty_data(self):
        """Test for ensuring data with any empty fields are not processed."""
        request_data = {
                "bookname" : "",
                "author" : "mock",
                "price" : 10,
                "category" : "sport",
                "quantity" :8,
                "agegroup" : "9-12"
            }

        # make request and process response
        response = self.client().post('/books', json=request_data,headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))

        # Assertions
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_books(self):
        """Test for updating book."""
        mock_data = {
                "bookname" : "Mockname",
                "author" : "mock",
                "price" : 10,
                "category" : "fiction",
                "quantity" :8,
                "agegroup" : "9-12"
            }
        response = self.client().patch('/books/6', json=mock_data, headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))

        # asserions to ensure successful request
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Book updated successfully!')

    def test_delete_book_with_valid_id(self):
        """Tests deletion of book with valid id"""
        # this tests an invalid id
        response = self.client().delete('/books/7', headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 7)

    def test_delete_book_with_invalid_header(self):
        """Tests deletion of book with valid id"""
        # this tests an invalid id
        headers = {
                    'Authorization' : 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjExLW1uM3NIQ2taSHJDX0J0LXFmNyJ9.eyJpc3MiOiJodHRwczovL2Rldi00MzUwYWlqZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwYjIyOWMyZWIzMDMwMDE5Yzg2NjczIiwiYXVkIjoiYm9va3Nob3AiLCJpYXQiOjE1OTQ1NjU0OTEsImV4cCI6MTU5NDYzNzQ5MSwiYXpwIjoiRUZneGxxdFM5dDFVdDdSbmhucVR5bHRwZjNDdjRuT0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpib29rcyIsInBhdGNoOmJvb2tzIl19.kk3qCREfz1WIABeTYPN_hTHHpMX1YYVYX85fdlBELk9M9tqHS_yCDDpIy71TIgjmT0W5MhcoCyeGkJ92VOFUmPB63xxW2t1e5mcrSmbh7aXecTSrCWGJe8M6ynLS0tXnS6CZHbB4l_IndcPRrGmajUFkPtSRyfIc0NScPZiI2OmJ-yhnjxbScv4tEBePMv-UNO1GnnhGRdCXtFZiLFXtZ3QLsrBC1HsQSYNNCIt-t8n001QC_DrRDAokUj2t0F-q1TxxPIB_5oOORpVUmoCSg673xhbySw7kD7jdDz69EXlmORczcbRoahPUg8QQlQwbGgvw1tGzswj9uvBa7AUiCw'
                  } 
        response = self.client().delete('/books/7', headers=headers)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header must start with "Bearer".')

    def test_delete_book_with_invalid_permission(self):
        """Tests deletion of book with valid id"""
        # this tests an invalid id
        headers = {
                    'Authorization' : 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjExLW1uM3NIQ2taSHJDX0J0LXFmNyJ9.eyJpc3MiOiJodHRwczovL2Rldi00MzUwYWlqZy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwYjIyOWMyZWIzMDMwMDE5Yzg2NjczIiwiYXVkIjoiYm9va3Nob3AiLCJpYXQiOjE1OTQ1NjU0OTEsImV4cCI6MTU5NDYzNzQ5MSwiYXpwIjoiRUZneGxxdFM5dDFVdDdSbmhucVR5bHRwZjNDdjRuT0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpib29rcyIsInBhdGNoOmJvb2tzIl19.kk3qCREfz1WIABeTYPN_hTHHpMX1YYVYX85fdlBELk9M9tqHS_yCDDpIy71TIgjmT0W5MhcoCyeGkJ92VOFUmPB63xxW2t1e5mcrSmbh7aXecTSrCWGJe8M6ynLS0tXnS6CZHbB4l_IndcPRrGmajUFkPtSRyfIc0NScPZiI2OmJ-yhnjxbScv4tEBePMv-UNO1GnnhGRdCXtFZiLFXtZ3QLsrBC1HsQSYNNCIt-t8n001QC_DrRDAokUj2t0F-q1TxxPIB_5oOORpVUmoCSg673xhbySw7kD7jdDz69EXlmORczcbRoahPUg8QQlQwbGgvw1tGzswj9uvBa7AUiCw'
                  } 
        response = self.client().delete('/books/7', headers=headers)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()