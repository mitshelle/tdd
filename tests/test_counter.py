"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 
import json


class CounterTest(TestCase):

    def setUp(self):
        self.client = app.test_client()
        
    """Counter tests"""
    def test_create_a_counter(self):
     """It should create a counter"""
     
     result = self.client.post('/counters/foo')
     self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should return an error for updates"""
        # create counter
        client = app.test_client()
        result = client.post('/counters/updateCounter')
        # check return success code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # check baseline
        baseReq = result.get_json()['updateCounter']
        self.assertEqual(baseReq, 0)
        # update counter
        update = client.put('/counters/updateCounter')
        # check greater than 0 
        baseReq = update.get_json()['updateCounter']
        self.assertEqual(baseReq, 1)
        # check return success code
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        # check if not exist yet
        update = client.put('/counters/updateCounter2')
        # check return success code
        self.assertEqual(update.status_code, status.HTTP_204_NO_CONTENT)

    def test_read_a_counter(self):
        """It should return an error for reading"""
        # create counter
        client = app.test_client()
        client.post('/counters/readCounter')
        # update counter
        client.put('/counters/readCounter')
        getResult = client.get('/counters/readCounter')
        # check return success code
        self.assertEqual(getResult.status_code, status.HTTP_200_OK)
        # does not exist check
        getResult = client.get('/counters/readCounter2')
        # check return success code
        self.assertEqual(getResult.status_code, status.HTTP_404_NOT_FOUND)

