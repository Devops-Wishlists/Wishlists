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
class TestOrders(unittest.TestCase):
    """ Test Cases for Orders """

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
        Order.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_wishlist(self):
        """ Create a wishlist and assert that it exists """
        wishlist = Wishlist(customer_id=1, wishlist_name = "subscription" ,)

        self.assertEqual(wishlist.id, None)
        self.assertEqual(wishlist.customer_id, 1)
        self.assertEqual(wishlist.wishlist_name, "subscription")

    def test_add_an_wishlist(self):
        """ Create a Wishlist and add it to the database """
        date = datetime.now()
        wishlists = wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = Wishlist(customer_id=1, wishlist_name = "subscription")
        self.assertEqual(wishlist.id, None)
        wishlist.save()

        self.assertEqual(wishlist.id, 1)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

    def test_get_or_404(self):
        """ Get_or_404 function with nonexistent ID """
        self.assertRaises(NotFound, Wishlist.get_or_404, 1)

    def test_non_dict_raises_error(self):
        """ Pass invalid data structure deserialize """
        data = [1,2,3]
        wishlist = Wishlist()

        with self.assertRaises(DataValidationError):
            order.deserialize(data)

    def test_invalid_key_raises_error(self):
        """ Try to pass invalid key """
        data = {"id": 1, "wishlist_name": subscription, "shipped": 1}

        with self.assertRaises(DataValidationError):
            order = Order()
            order.deserialize(data)

    def test_repr(self):
        """ Test that string representation is correct """
        date = datetime.now()
        order = Order(customer_id=1, date=date, shipped=True)
        order.save()

        self.assertEqual(order.__repr__(), "<Order>")

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()