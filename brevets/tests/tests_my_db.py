"""
Nose tests for my_db.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
from my_db import insert_brevets
from my_bd import get_brevets
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def test_insert_brevets():
    # Test inserting brevets into the database
    control_data = [ {"kilometers" : 0, "open" :"2021-01-01T00:00" , "close" : "2021-01-01T01:00"}, ]
    total_distance = "200"
    date_time = "2021-01-01T00:00"

    # Call the insert_brevets function
    inserted_id = insert_brevets(total_distance, date_time, control_data)

    # Check if the insertion was successful 
    assert inserted_id is not None

def test_get_brevets():
    # Test retrieving brevets from the database
    
    control_data = [ {"kilometers" : 0, "open" :"2022-04-01T00:00" , "close" : "2022-04-01T01:00"}, ]
    total_distance = "200"
    date_time = "2022-04-01T00:00"

    # Insert data for testing
    inserted_id = insert_brevets(total_distance, date_time, control_data)

    # Call the get_brevets function
    retrieved_brevets = get_brevets()

    # Check if the retrieval was successful 
    assert result[0][0]["km"] ==  0
    assert result[0][0]["open"] == "2022-04-01T00:00"
    assert result[0][0]["close"] == "2022-04-01T01:00"
    assert result[1] == "2022-04-01T00:00"
    assert result[2] == 200
