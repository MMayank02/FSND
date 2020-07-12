import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
import json

database_path = os.environ['DATABASE_URL']

if not database_path:
    database_name = "testcaps"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name, encoding = 'utf8') 

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config.from_object('config')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PGCLIENTENCODING"] = 'UTF-8'
    db.app = app
    migrate = Migrate(app,db)
    db.init_app(app)
#   db.create_all()
    

'''
Books
'''

class Books(db.Model):  
  __tablename__ = 'books'

  id = Column(Integer, primary_key=True)
  bookname = Column(String, nullable=False)
  author = Column(String, nullable=False)
  price = Column(Integer, nullable=False)
  quantity = Column(Integer, nullable=False)
  category_id = Column(Integer, db.ForeignKey('category.id'))
  age_id = Column(Integer, db.ForeignKey('kidsage.id'))


  def __init__(self, bookname, author, price, quantity, category_id, age_id):
    self.bookname = bookname
    self.author = author
    self.price = price
    self.quantity = quantity
    self.category_id = category_id
    self.age_id = age_id


  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'bookname': self.bookname,
      'author' : self.author,
      'price': self.price,
      'quantity':self.quantity,
      'category_id': self.category_id,
      'age_id': self.age_id,
    }

'''
Category
'''

class Category(db.Model):  
  __tablename__ = 'category'

  id = Column(Integer, primary_key=True)
  type = Column(String, nullable=False)
  bookss = db.relationship('Books', backref='types', lazy=True)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }

class Kidsage(db.Model):  
  __tablename__ = 'kidsage'

  id = Column(Integer, primary_key=True)
  agegroup = Column(String, nullable=False)
  books = db.relationship('Books', backref='ages', lazy=True)

  def __init__(self, type):
    self.agegroup = agegroup

  def format(self):
    return {
      'id': self.id,
      'agegroup': self.agegroup
    }