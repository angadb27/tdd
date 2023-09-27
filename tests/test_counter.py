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

class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)
        
        def test_update_a_counter(self):
            """It should update a counter"""
            result = self.client.post('/counters/bar')
            self.assertEqual(result.status_code, status.HTTP_201_CREATED)

            base_result = self.client.get('/counters/bar')
            base_value = json.loads(base_result.data)["bar"]

            update_result = self.client.put('/counters/bar')
            self.assertEqual(update_result.status_code, status.HTTP_200_OK)

            new_result = self.client.get('/counters/bar')
            new_value = json.loads(new_result.data)["bar"]
            self.assertEqual(new_value, base_value + 1)

        def test_read_a_counter(self):
            self.client.post('/counters/bar')
            # Read the counter
            result = self.client.get('/counters/bar')
            self.assertEqual(result.status_code, status.HTTP_200_OK)
            value = json.loads(result.data)["bar"]
            self.assertEqual(value, 1) 

    