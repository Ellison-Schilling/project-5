"""
Description: Contains all logic dealing with mongo db, submit, and display. Acts as an inbetween for calc.html and flask_brevet.py
for mongo database storing. Isolation allows for easier testing.
Author: Ellison Schilling
"""
import os
import logging

import flask
from flask import request

from pymongo import MongoClient

# Set up Flask app
app = flask.Flask(__name__)
app.debug = True
app.logger.setLevel(logging.DEBUG)

# Set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

# Use database "brevet"
db = client.brevets

# Use collection "rows" in the databse
collection = db.rows

##################################################
################ MongoDB Functions ############### 
##################################################


def get_brevets():
    """
    Obtains the newest document in the "rows" collection in database "brevets".
    Returns a list of dictionaries for each field.
    """
    # Get documents (brevets) in our collection (rows),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    rows = collection.find().sort("_id", -1).limit(1)

    # lists is a PyMongo cursor, which acts like a pointer.
    # We need to iterate through it, even if we know it has only one entry:
    for row in rows:
        # We store all of our brevets as documents with a single field row:
        ## every row has 6 fields
        ### miles: float  
        ### kilometers: float  
        ### location: string 
        ### open: float
        ### close: float
        return row["brevets"]


def insert_brevets(brevets):
    """
    Inserts a new brevet list of dictionaries into the database "brevets", under the collection "brevets".
    
    Inputs a list of dictionaries 

    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    output = collection.insert_one({
        "brevets": brevets})
    _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    print("\n\nSTRING IDDD\n" + str(_id), flush=True)
    return str(_id)

