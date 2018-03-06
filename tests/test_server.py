"""
Wishlists API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""

import unittest
import os
import json
import logging
from datetime import datetime
from flask_api import status    # HTTP Status Codes
from mock import MagicMock, patch

from models import Item, Wishlist, DataValidationError, db
import server


DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415


class TestServer(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
    	""" Run once before all tests """
    	server.app.debug = False
    	server.initialize_logging(logging.INFO)
        # Set up the test database
        server.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

	def setUp(self):
		# Set up the test database
		server.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test.db'
		self.app = server.app.test_client()

	def tearDown(self):
		return

	def test_index(self):
		resp = self.app.get('/')
		self.assertEqual( resp.status_code, status.HTTP_200_OK )
		self.assertTrue ('Wishlist REST API Service' in resp.data)

    def test_create_wishlist(self):
        """ Create a new Wishlist and Items handling"""
        # save the current number of wishlists for later comparison
        wishlist_count = self.get_wishlist_count()
        item_count = self.get_item_count()
        # add a new wishlist. wishlist id is 3 since there are 2 wishlists initially
        new_wishlist = {'customer_id': 1, 'wishlist_name': "alex's wishlist"}
        new_wishlist['items'] = [{"wishlist_id": 3, "product_id": 3, "name": "Alex", "description": "no description"}]
        data = json.dumps(new_wishlist)
        resp = self.app.post('/wishlists', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)

        """
        Check the data is correct by verifying that the customer_id and
        wishlist_id are correct
        """
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['customer_id'], 1)
        self.assertEqual(new_json['items'][0]["wishlist_id"], 3)
        self.assertEqual(len(new_json['items']), 1)
        """
        Check that response is correct for the wishlist and that wishlist count has
        increased to reflect new wishlist
        """
        resp = self.app.get('/wishlists')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), wishlist_count + 1)
        new_json_wishlists = new_json.copy()
        new_json_wishlists.pop('items')
        self.assertIn(new_json_wishlists, data)
        """
        Check that response is correct for the wishlist's items and that
        item count has increased to reflect items in the new wishlist
        """
        resp = self.app.get('/items')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), item_count + 1)
        new_json_items = new_json.pop('items')[0]
        self.assertIn(new_json_items, data)

    def test_get_item_list(self):
        """ Get a list of Items """
        resp = self.app.get('/items')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 3)


    def test_delete_item(self):
        """ Test deleting an Item """
        item = Item()
        # Using one of the existing test Items from setup
        item.id = 2
        # Save the current number of items for assertion
        item_count = self.get_item_count()
        resp = self.app.delete('/items/{}'.format(item.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_item_count()
        self.assertEqual(new_count, item_count - 1)

######################################################################
# UTILITY FUNCTIONS
######################################################################

    def get_item_count(self):
        """ save the current number of items """
        resp = self.app.get('/items')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)

    def get_wishlist_count(self):
        """ save the current number of wishlists """
        resp = self.app.get('/wishlists')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)


######################################################################
# MAIN
######################################################################
if __name__ == '__main__':
    unittest.main()
