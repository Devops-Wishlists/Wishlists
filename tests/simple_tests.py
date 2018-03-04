import unittest
import json
import server
import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    
from werkzeug.exceptions import NotFound

class TestServer(unittest.TestCase):

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
