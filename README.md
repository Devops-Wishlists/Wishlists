# wishlists

[![Build Status](https://travis-ci.org/Devops-Wishlists/wishlists.svg?branch=master)](https://travis-ci.org/Devops-Wishlists/wishlists)
[![codecov](https://codecov.io/gh/Devops-Wishlists/wishlists/branch/master/graph/badge.svg)](https://codecov.io/gh/Devops-Wishlists/wishlists)

Wishlists Team for Devops_2018_Spring


## Prerequisite Installation using Vagrant

The first step is to install VirtualBox and Vagrant:

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Clone the project to your development folder and create your Vagrant vm

    $ git clone https://github.com/Devops-Wishlists/wishlists.git
    $ cd wishlists
    $ vagrant up

Once the VM is up you can use it with:

    $ vagrant ssh
    $ cd /vagrant
    $ python server.py

When you are done, you can use `Ctrl+C` to stop the server and then exit and shut down the vm with:

    $ exit
    $ vagrant halt


## Testing code
To test the code, it is easiest to use Vagrant. After installation,
run these commands.

```
	vagrant up
	vagrant ssh
	cd /vagrant
	nosetests
```

The test suite 'nosetests' tests the multiple functionalities offered by the
service, which are listed below.
For furthur information on the tests, type the following command

```
	coverage report -m
```

The service can be started and used with the following command

```
	python server.py
```

The service will be located on "http://localhost:5000"

## Available calls

The following REST calls are supported by this service

-  CREATE - takes the JSON and creates the wishlist and item 
   - `POST http://localhost:5000/wishlists` 
-  GET - Gets the details of a specific wishlist 
   - `GET http://localhost:5000/wishlists/{wishlist_id}`  
-  GET - Get details of a specific item: 
   - `GET http://localhost:5000/items/{item_id}`
-  LIST - All wishlists in the system: 
   - `GET http://localhost:5000/wishlists`
-  LIST - All items in the system: 
   - `GET http://localhost:5000/items`
-  LIST - Items from a specified wishlist: 
   - `GET http://localhost:5000/wishlists/{wishlist_id}/items`
-  DELETE - deletes a wishlist and its items: 
   - `DELETE http://localhost:5000/wishlists/{wishlist_id}`
-  DELETE - deletes an item: 
   - `DELETE http://localhost:5000/items/{item_id}`
-  PUT - update a wishlist:
   - `PUT http://localhost:5000/wishlists/{id}`
-  PUT - update an item:
   - `PUT http://localhost:5000/items/{item_id}`
-  GET - Get an item description:
   - `GET http://localhost:5000/items/{item_id}/description`
-  POST - add an item description:
   - `PUT http://localhost:5000/items/{item_id}/description`   
-  ACTION - clear all items from a wishlist:
   - `PUT http://localhost:5000/wishlists/{wishlist_id}/clear`   
-  QUERY - query for a wishlist based on its name:
   - `GET http://localhost:5000/wishlists?keyword=<value>`