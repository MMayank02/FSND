import os, logging
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = False
logging.basicConfig(level=logging.DEBUG)
# Connect to the database

# TODO IMPLEMENT DATABASE URL 
# Done
logging.basicConfig(level=logging.DEBUG)

SQLALCHEMY_DATABASE_URI = "postgres://{}/{}".format('localhost:5432', 'testcaps', encoding = 'utf8') 
SQLALCHEMY_TRACK_MODIFICATIONS = False