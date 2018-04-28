"""
Test cases for Wishlist Model
Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from datetime import datetime

from models import Wishlist, DataValidationError, db
from werkzeug.exceptions import NotFound
from server import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestWishlists(unittest.TestCase):
    """ Test Cases for Wishlists """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Wishlist.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_wishlist(self):
        """ Create a wishlist and assert that it exists """
        wishlist = Wishlist(customer_id=1, wishlist_name = "subscription")

        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.customer_id, 1)
        self.assertEqual(wishlist.wishlist_name, "subscription")

    def test_add_an_wishlist(self):
        """ Create a Wishlist and add it to the database """
        date = datetime.now()
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = Wishlist(customer_id=1, wishlist_name = "subscription")
        self.assertEqual(wishlist.id, None)
        wishlist.save()

        self.assertEqual(wishlist.id, 1)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

    def test_delete_an_wishlist(self):
        """ Delete a Wishlist """
        wishlist = Wishlist(customer_id=1, wishlist_name = "subscription")
        wishlist.save()
        self.assertEqual(len(Wishlist.all()), 1)

        wishlist.delete()
        self.assertEqual(len(Wishlist.all()), 0)

    def test_serialize_a_wishlist(self):
        """ Test serialization of a Wishlist """
        wishlist = Wishlist(customer_id=1, wishlist_name = "subscription")
        data = wishlist.serialize()

        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)

        self.assertIn('customer_id', data)
        self.assertEqual(data['customer_id'], 1)
        self.assertIn('wishlist_name', data)
        self.assertEqual(data['wishlist_name'], "subscription")   

    def test_deserialize_a_wishlist(self):
        """ Test deserialization of a Wishlist """
        data = {"id": 1, "customer_id": 1, "wishlist_name": "subscription"}
        wishlist = Wishlist()
        wishlist.deserialize(data)

        self.assertNotEqual(wishlist, None)
        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.customer_id, 1)
        self.assertEqual(wishlist.wishlist_name, "subscription") 


    def test_fetch_all_wishlists(self):
        """ Test fetching all Wishlists """
        wishlist1 = Wishlist(customer_id=1, wishlist_name = "subscription")
        wishlist1.save()
        wishlist2 = Wishlist(customer_id=2, wishlist_name = "liked")
        wishlist2.save()
        Wishlist.all()

        self.assertEqual(len(Wishlist.all()), 2)

    def test_repr(self):
        """ Test that string representation is correct """
        wishlist = Wishlist(customer_id=1, wishlist_name = 'shop list')
        wishlist.save()

        self.assertEqual(wishlist.__repr__(), "<Wishlist>")

    def test_404(self):
        """ Test Get_or_404 function with nonexistent ID """
        self.assertRaises(NotFound, Wishlist.get_or_404, 1)

    def test_invalid_key_error(self):
        """ Test for passing invalid key """
        data = {"id": 1, "wishlist_name": 'shop list'}

        with self.assertRaises(DataValidationError):
            wishlist = Wishlist()
            wishlist.deserialize(data)
    
    def test_non_data_raises_error(self):
        """ Test for invalid data structure deserialize """
        data = [1,2,3,4,5]
        wishlist = Wishlist()

        with self.assertRaises(DataValidationError):
            wishlist.deserialize(data)

    def test_find_by_customer_id(self):
        """ Find wishlists by customer_id """
        wishlist = Wishlist(customer_id=1, wishlist_name = 'computer')
        wishlist.save()
        wishlist1 = Wishlist.find_by_customer_id(wishlist.customer_id)
        self.assertEqual(wishlist1[0].customer_id, wishlist.customer_id)

    def test_find_by_wishlist_name(self):
        """ Find wishlists by wishlist_name """
        wishlist = Wishlist(customer_id=1, wishlist_name = 'computer')
        wishlist.save()
        wishlist1 = Wishlist.find_by_wishlist_name(wishlist.wishlist_name)
        self.assertEqual(wishlist1[0].wishlist_name, wishlist.wishlist_name)






######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()