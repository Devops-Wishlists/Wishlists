# wishlists

[![Build Status](https://travis-ci.org/Devops-Wishlists/wishlists.svg?branch=master)](https://travis-ci.org/Devops-Wishlists/wishlists)
[![codecov](https://codecov.io/gh/Devops-Wishlists/wishlists/branch/master/graph/badge.svg)](https://codecov.io/gh/Devops-Wishlists/wishlists)

Wishlists Team for Devops_2018_Spring

## Testing code
To test the code, it is easiest to use Vagrant. After installation,
run these commands.

'''
	vagrant up
	vagrant ssh
	cd /vagrant
	nosetests
'''

The test suite 'nosetests' tests the multiple functionalities offered by the
service, which are listed below.
For furthur information on the tests, type the following command

'''
	coverage report -m
'''

The service can be started and used with the following command

'''
	python server.py
'''

The service will be located on "http://localhost:5000"

## Available calls

The following REST calls are supported by this service
GET /										- return root URL
GET /wishlists 								- return all wishlists
POST /wishlists 							- create a new wishlist
GET /wishlists/{wishlist_id}				- return a specific wishlist
DELETE /wishlists/{wishlist_id}				- delete a specific wishlist
PUT /wishlists/{wishlist_id}/clear			- clear all items on a wishlist
GET /items									- return all items
GET /items/{item_id}						- return a single item
DELETE /items/{item_id}						- delete a single item
GET /wishlists/{wishlist_id}/items			- return all items on a wishlist
PUT /wishlists/{wishlist_id}/items/{item_id} 	- update an item's id
GET /items/{item_id}/description			- Get an item's description
POST /items/{item_id}/description			- Add description to an item
PUT /wishlists/{wishlist_id}/clear			- Clear all items from a wishlist
GET /wishlists/search						- Search a wishlist by its name

