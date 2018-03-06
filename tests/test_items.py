"""
Test cases for Item Model
Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from models import Item, DataValidationError, db
from werkzeug.exceptions import NotFound
from server import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestItems(unittest.TestCase):
    """ Test Cases for Items """

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
        Item.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_an_item(self):
        """ Create a item and assert that it exists """
        item = Item(product_id=1, name="toothpaste", description="toothpaste for 2")

        self.assertEqual(item.id, None)
        self.assertEqual(item.product_id, 1)
        self.assertEqual(item.name, "toothpaste")
        self.assertEqual(item.description,"toothpaste for 2")

    def test_add_an_item(self):
        """ Create an Item and add it to the database """
        items = Item.all()
        self.assertEqual(items, [])
        item = Item(wishlist_id=1, product_id=1, name="toothpaste", description="toothpaste for 2")
        self.assertEqual(item.id, None)
        item.save()

        self.assertEqual(item.id, 1)
        items = Item.all()
        self.assertEqual(len(items), 1)

    def test_update_an_item(self):
        """ Update an Item """
        item = Item(wishlist_id=1, product_id=1, name="toothpaste", description="toothpaste for 2")
        item.save()
        self.assertEqual(item.id, 1)

        item.description= "toothpaste for 1" 
        item.save()

        items = Item.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].description, "toothpaste for 1")

    def test_delete_an_item(self):
        """ Delete an Item """
        item = Item(wishlist_id=1, product_id=1, name="toothpaste", description="toothpaste for 2")
        item.save()
        self.assertEqual(len(Item.all()), 1)

        item.delete()
        self.assertEqual(len(Item.all()), 0)


    def test_non_dict_raises_error(self):
        """ Pass invalid data structure deserialize """
        data = [1,2,3]
        item = Item()
        wishlist_id = 1

        with self.assertRaises(DataValidationError):
            item.deserialize(data, wishlist_id)




######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()