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
import json
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()
        # Resetting the counters before each test
        with app.app_context():
            global COUNTERS
            COUNTERS = {}

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post('/counters/bar_create')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar_duplicate')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar_duplicate')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)
        
    def test_update_a_counter(self):
        """It should update a counter"""
        result = self.client.post('/counters/bar_update')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        base_result = self.client.get('/counters/bar_update')
        base_value = json.loads(base_result.data)["bar_update"]

        update_result = self.client.put('/counters/bar_update')
        self.assertEqual(update_result.status_code, status.HTTP_200_OK)

        new_result = self.client.get('/counters/bar_update')
        new_value = json.loads(new_result.data)["bar_update"]
        self.assertEqual(new_value, base_value + 1)

        no_result = self.client.put('/counters/no_result_update')
        self.assertEqual(no_result.status_code, status.HTTP_404_NOT_FOUND)
        response_data = json.loads(no_result.data)
        self.assertEqual(response_data["error"], "Counter not found")

    def test_read_a_counter(self):
        self.client.post('/counters/bar_read')
        """It should read a counter"""
        result = self.client.get('/counters/bar_read')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        value = json.loads(result.data)["bar_read"]
        self.assertEqual(value, 0) 

        no_result = self.client.get('/counters/no_result_read')
        self.assertEqual(no_result.status_code, status.HTTP_404_NOT_FOUND)
        response_data = json.loads(no_result.data)
        self.assertEqual(response_data["error"], "Counter not found")
    
    def test_delete_a_counter(self):
        """It should delete a counter"""
        self.client.post('/counters/bar_delete')
        
        delete_result = self.client.delete('/counters/bar_delete')
        self.assertEqual(delete_result.status_code, status.HTTP_204_NO_CONTENT)
        
        # Test for deletting a counter that does not exist
        no_delete = self.client.delete('/counters/no_result_delete')
        self.assertEqual(no_delete.status_code, status.HTTP_404_NOT_FOUND)
        response_data = json.loads(no_delete.data)
        self.assertEqual(response_data["error"], "Counter not found")