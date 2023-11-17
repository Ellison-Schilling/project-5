"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request

import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import sys

import logging

import os
from pymongo import MongoClient

###
# Globals
###
app = flask.Flask(__name__)
app.debug = True
app.logger.setLevel(logging.DEBUG)
CONFIG = config.configuration()

# Set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

# Use database "brevet_database"
db = client.brevet_database

# Use collection "brevet_collection" in the databse
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





###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    # Arugments
    km = request.args.get('km', 999, type=float)
    date = request.args.get('date', 0, type=str)

    distance = request.args.get('distance', 0, type=float)  # Request the time given
    time = request.args.get('time', 0, type=str)    # Request the time specified

    # Checking
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    # Formating date_time
    date_time = date + ' ' + time + ':00'   # Fix how the date is put in to include the time as well
    arrow_time = arrow.get(date_time, 'YYYY-MM-DD HH:mm:ss')    # Formats the date_time into arrow

    open_time = arrow.get(acp_times.open_time(km, distance, arrow_time))
    
    # Happens on invalid input simply does not return anything helpful
    if open_time == None:
        return None

    open_time = arrow.get(open_time)

    close_time = acp_times.close_time(km, distance, arrow_time)
    
    # Happens on invalid input does not return anything helpful
    if open_time == None:
        return None

    close_time = arrow.get(close_time)  

    result = {"open": open_time.format('YYYY-MM-DD HH:mm'), "close": close_time.format('YYYY-MM-DD HH:mm')}

    return flask.jsonify(result=result)

@app.route("/submit", methods=["POST"])
def submit():
    """
    /submit : inserts a brevet table into the database.

    Accepts POST requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        total_distance = input_json["total_distance"]   # Should be a string containing the total distance of the race 
        date_time = input_json["date_time"]         # Should be a string containing the date_time
        control_data = input_json["control_data"]   # Should be a list of dictionaries of brevet information

        brevets_id = insert_brevets(total_distance, date_time, control_data)  # Make a call to our database file to store the brevets

        return flask.jsonify(result={},
                        message="Submitted!", 
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=brevets_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')


@app.route("/display")
def display():
    """
    /display : fetches the latest brevets from the database.

    Accepts GET requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        total_distance, date_time, control_data = get_brevets()   # Fetch the data from the database
        return flask.jsonify(
                result={"total_distance" : total_distance,  # Return the data to json
                         "date_time" : date_time,
                         "control_data" : control_data
                        }, 
                status=1,
                message="Successfully fetched the brevets!")
    except:
        return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't fetch any brevets!")


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
