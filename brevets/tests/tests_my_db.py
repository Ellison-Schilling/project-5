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
    brevets_data = [
        {"miles": 3.10685, "kilometers": 5, "location": "Kansas", "open": "2023-01-01T00:00:00", "close": "2023-01-01T01:00:00"},
        {"miles": 5, "kilometers": 8.04672, "location": "Idaho", "open": "2023-01-01T02:00:00", "close": "2023-01-01T03:00:00"}
    ]

    # Call the insert_brevets function
    inserted_id = insert_brevets(brevets_data)

    # Check if the insertion was successful 
    assert inserted_id is not None

def test_get_brevets():
    # Test retrieving brevets from the database
    brevets_data = [
        {"miles": 3.10685, "kilometers": 5, "location": "Kansas", "open": "2023-01-01T00:00:00", "close": "2023-01-01T01:00:00"},
        {"miles": 5, "kilometers": 8.04672, "location": "Idaho", "open": "2023-01-01T02:00:00", "close": "2023-01-01T03:00:00"}
    ]

    # Insert data for testing
    insert_brevets(brevets_data)

    # Call the get_brevets function
    retrieved_brevets = get_brevets()

    # Check if the retrieval was successful 
    assert len(retrieved_brevets) == len(brevets_data)
