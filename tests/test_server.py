import unittest
import json
import server
import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    
from werkzeug.exceptions import NotFound


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
