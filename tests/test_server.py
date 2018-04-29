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
        """ Test the Index """
        resp = self.app.get('/') 
        self.assertIn('Wishlist REST API Service', resp.data)

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

    def test_get_wishlist_list(self):
        """ Test getting a list of Wishlists """
        resp = self.app.get('/wishlists')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_get_item_list(self):
        """ Test getting a list of Items """
        resp = self.app.get('/items')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 3)

    def test_get_wishlist_item_list(self):
        """ Test getting a list of Items from one specific Wishlist """
        wishlist = Wishlist.find_by_customer_id(1)[0]
        print wishlist.id
        resp = self.app.get('/wishlists/{}/items'.format(wishlist.id),
                            content_type='application/json')
        print json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_create_wishlist(self):
        """ Test creating a new Wishlist"""
        # save the current number of wishlists for later comparison
        wishlist_count = self.get_wishlist_count()
        item_count = self.get_item_count()

        # add a new wishlist. wishlist id is 3 since there are 2 wishlists initially
        new_wishlist = {'customer_id': 1, 'wishlist_name': "alex's wishlist"}
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

        """
        Check that response is correct for the wishlist and that wishlist count has
        increased to reflect new wishlist
        """
        resp = self.app.get('/wishlists')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), wishlist_count + 1)
        new_json_wishlists = new_json.copy()
        self.assertIn(new_json_wishlists, data)

    def test_get_wishlist(self):
        """Test getting a wishlist"""
        wishlist_id = Wishlist.find_by_customer_id(2)[0].id
        resp = self.app.get('/wishlists/{}'.format(wishlist_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.data)['wishlist_name'], 'beverage')

    def test_get_wishlist_not_found(self):
        """Test getting a wishlist thats not found """
        resp = self.app.get('/wishlists/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item(self):
        """Test getting an item"""
        item = Item.find_by_name('toilet paper')[0]
        resp = self.app.get('/items/{}'.format(item.id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(resp.data)['name'],'toilet paper')

    def test_get_item_not_found(self):
        """Test getting an item thats not found """
        resp = self.app.get('/items/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_item(self):
        """ Deleting an Item from an Wishlist"""
        item = Item.find_by_name('toilet paper')[0]

        # Save the current number of items for assertion
        item_count = self.get_item_count()
        resp = self.app.delete('/wishlists/{}/items/{}'.format(item.wishlist_id, item.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_item_count()
        self.assertEqual(new_count, item_count - 1)

        resp = self.app.delete('/wishlists/{}/items/{}'.format(5, item.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.app.delete('/wishlists/{}/items/{}'.format(2, 1),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

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

    def test_clear_wishlist(self):
        """ Test clearing a Wishlist """
        new_wishlist = {'customer_id': 1, 'wishlist_name': "alex's wishlist"}
        data = json.dumps(new_wishlist)
        resp = self.app.post('/wishlists', data=data, content_type='application/json')
        new_items = {"wishlist_id": 3, "product_id": 3, "name": "soda", "description": "I need some soft drinks"}
        data = json.dumps(new_items)
        resp = self.app.post('/wishlists/3/items', data=data, content_type='application/json')

        items = Item.find_by_wishlist_id(3)
        self.assertEqual(items[0].wishlist_id, 3)
        self.assertEqual(len(list(items)), 1)
        resp = self.app.put('/wishlists/3/clear',content_type = 'application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        items = Item.find_by_wishlist_id(3)
        self.assertEqual(len(list(items)), 0)


    def test_update_item(self):
        """Test updating an Item already exists """
        item = Item.find_by_name('toilet paper')[0]
        new_item = {'wishlist_id': 1, 'product_id': 2, 'name': "diet coke", 'description': 'I need a coke'}
        data = json.dumps(new_item)

        resp = self.app.put('/wishlists/{}/items/{}'.format(new_item['wishlist_id'], item.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['name'], 'diet coke')

    def test_update_item_not_found(self):
        """Test Updating an item doesn't exist"""
        new_item = {'wishlist_id': 0, 'product_id': 2, 'name': "diet coke", 'description': 'I need a coke'}
        data = json.dumps(new_item)
        resp = self.app.put('/wishlists/{}/items/100'.format(new_item['wishlist_id']), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item_no_name(self):
        """Test updating an item without giving a name"""
        item = Item.find_by_name('toilet paper')[0]
        new_item = {'wishlist_id': 0, 'product_id': 2, 'description': 'I need a coke'}
        data = json.dumps(new_item)
        resp = self.app.put('/wishlists/{}/items/{}'.format(new_item['wishlist_id'], item.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_item_description(self):
        """Test reading item description"""
        item = Item.find_by_name('toilet paper')[0]
        resp = self.app.get('/wishlists/{}/items/{}/description'.format(item.wishlist_id,item.id), content_type ='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        description = 'I need a toilet paper'
        self.assertEqual(new_json['description'],description)

    def test_update_wishlist(self):
        """Test updating a Wishlist already exists """
        wishlist = Wishlist.find_by_customer_id(1)[0]
        new_wishlist = {'customer_id': 1, 'wishlist_name': "alex's wishlist"}
        new_wishlist['items'] = [{"wishlist_id": 3, "product_id": 3, "name": "soda", "description": "I need some soft drinks"}]
        data = json.dumps(new_wishlist)

        resp = self.app.put('/wishlists/{}'.format(wishlist.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['wishlist_name'], "alex's wishlist")

    def test_update_wishlist_not_found(self):
        """Test updating a existing Wishlist doesn't exist"""
        new_wishlist = {'customer_id': 1, 'wishlist_name': "alex's wishlist"}
        new_wishlist['items'] = [{"wishlist_id": 3, "product_id": 3, "name": "soda", "description": "I need some soft drinks"}]
        data = json.dumps(new_wishlist)

        resp = self.app.put('/wishlists/0', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_wishlist_no_name(self):
        """Test updating a existing Wishlist with no name"""
        wishlist = Wishlist.find_by_customer_id(1)[0]
        new_wishlist = {'customer_id': 1}
        '''new_wishlist['items'] = [{"wishlist_id": 3, "product_id": 3, "name": "soda", "description": "I need some soft drinks"}]'''
        data = json.dumps(new_wishlist)
        resp = self.app.put('/wishlists/{}'.format(wishlist.id), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_not_allowed(self):
        """Test calling a Method thats not Allowed """
        resp = self.app.post('/wishlists/0')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_wrong_content_type(self):
        """Test creating a wrong content type thats not Allowed """
        wishlist_count = self.get_wishlist_count()
        item_count = self.get_item_count()
        new_wishlist = {'customer_id': 1}
        '''new_wishlist['items'] = [{"wishlist_id": 3, "product_id": 3, "name": "soda", "description": "I need some soft drinks"}]'''
        data = json.dumps(new_wishlist)
        resp =self.app.post('/wishlists', data=data, content_type="text/plain")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_query_wishlist(self):
        """ Get wishlists with keywords """
        resp = self.app.get('/wishlists', query_string='keyword=beverage')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('beverage' in resp.data)
        self.assertFalse('computer' in resp.data)
        data = json.loads(resp.data)
        query_wishlists = data[0]
        self.assertEqual(query_wishlists['wishlist_name'], 'beverage')

    def test_query_customerid_wishlist(self):
        """ Get wishlists with customer_id """
        resp = self.app.get('/wishlists', query_string='customer_id=1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertTrue('grocery' in resp.data)
        self.assertFalse('computer' in resp.data)
        data = json.loads(resp.data)
        query_wishlists = data[0]
        self.assertEqual(query_wishlists['wishlist_name'], 'grocery')

######################################################################
# MAIN
######################################################################
if __name__ == '__main__':
    unittest.main()
