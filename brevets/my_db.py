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
db = client.brevet_database

# Use collection "rows" in the databse
collection = db.brevet_collection

##################################################
################ MongoDB Functions ############### 
##################################################


def get_brevets():
    """
    Obtains the newest document in the collection in brevet_database.
    Returns the total brevet distance, the date_time for the start of the race, and a dictionary of 
    brevet control data including the control distance, open time, and close time.
    """
    # Get documents in brevet_database in our collection brevet_collection,
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    brevet_collection = collection.find().sort("_id", -1).limit(1)

    # lists is a PyMongo cursor, which acts like a pointer.
    # We need to iterate through it, even if we know it has only one entry:
    for data in brevet_collection:
        # We store all of our brevets as documents with 3 fields:
        ## The first two fields only have one item, but the last has three
        
        ### total_distance: float  
        ### date_time : string

        ### control_data : dict
        ### control_distance
        ### open: float
        ### close: float
        return data["total_distance"], data["date_time"], data["control_data"]


def insert_brevets(total_distance, date_time, control_data):
    """
    Inserts a new brevet list of dictionaries into the database "brevets", under the collection "brevets".
    
    Inputs a list of dictionaries 

    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    output = collection.insert_one({
        "total_distance": total_distance, 
        "date_time" : date_time,
        "control_data": control_data})
    _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    return str(_id)

