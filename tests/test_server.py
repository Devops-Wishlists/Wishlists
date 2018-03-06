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

    def setUp(self):
        """ Runs before each test """
        server.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables

        item = Item(wishlist_id=1, product_id=1, name='toothpaste', description= 'I need a toothpaste').save()
        item = Item(wishlist_id=1, product_id=2, name='toilet paper', description= 'I need a toilet paper').save()
        item = Item(wishlist_id=2, product_id=3, name='beer', description= 'I need a drink').save()
        wishlist = Wishlist(customer_id=1, wishlist_name = 'grocery').save()
        wishlist = Wishlist(customer_id=2, wishlist_name = 'beverage').save()
        self.app = server.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

	def test_index(self):
		resp = self.app.get('/')
		self.assertEqual( resp.status_code, status.HTTP_200_OK )
		self.assertTrue ('Wishlist REST API Service' in resp.data)


    def test_get_wishlist_list(self):
        """ Get a list of Wishlists """
        resp = self.app.get('/wishlists')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_item_list(self):
        """ Get a list of Items """
        resp = self.app.get('/items')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 3)

    def test_get_wishlist_item_list(self):
        """ Get a list of Items from a Wishlist """
        wishlist = Wishlist.find_by_customer_id(1)[0]
        print wishlist.id
        resp = self.app.get('/wishlists/{}/items'.format(wishlist.id),
                            content_type='application/json')
        print json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_create_wishlist(self):
        """ Create a new Wishlist and Items handling"""
        # save the current number of wishlists for later comparison
        wishlist_count = self.get_wishlist_count()
        item_count = self.get_item_count()

        # add a new wishlist. wishlist id is 3 since there are 2 wishlists initially
        new_wishlist = {'customer_id': 1, 'wishlist_name': "alex's wishlist"}
        new_wishlist['items'] = [{"wishlist_id": 3, "product_id": 3, "name": "soda", "description": "I need some soft drinks"}]
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

    def test_get_item_list(self):
        """ Get a list of Items """
        resp = self.app.get('/items')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 3)

    def test_delete_wishlist(self):
        """ Test deleting a Wishlist """
        wishlist = Wishlist.find_by_customer_id(1)[0]
        # Save the current number of wishlists for assertion
        wishlist_count = self.get_wishlist_count()
        resp = self.app.delete('/wishlists/{}'.format(wishlist.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_wishlist_count()
        self.assertEqual(new_count, wishlist_count - 1)

    def test_get_wishlist_not_found(self):
        """ Get a wishlist thats not found """
        resp = self.app.get('/wishlists/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item_not_found(self):
        """ Get an item thats not found """
        resp = self.app.get('/items/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_item(self):
        """ Update an existing Item """
        item = Item.find_by_name('toilet paper')[0]
        new_item = {'wishlist_id': 1, 'product_id': 2, 'name': "diet coke", 'description': 'I need a coke'}
        data = json.dumps(new_item)

        resp = self.app.put('/wishlists/{}/items/{}'.format(new_item['wishlist_id'], item.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'diet coke')

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
