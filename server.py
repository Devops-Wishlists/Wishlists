import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import NotFound

from flask_sqlalchemy import SQLAlchemy

from model import Wishlist, Item, DataValidationError

app = Flask(__name__)

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

# dev config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'please, tell nobody... Shhhh'
app.config['LOGGING_LEVEL'] = logging.INFO

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=400, error='Bad Request', message=message), 400

@app.errorhandler(404)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=404, error='Not Found', message=message), 404

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=405, error='Method not Allowed', message=message), 405

@app.errorhandler(415)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=415, error='Unsupported media type', message=message), 415

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=500, error='Internal Server Error', message=message), 500


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Return something useful by default """
    return jsonify(name='Wishlist REST API Service', version='1.0'), HTTP_200_OK


######################################################################
# CREATE A NEW WISHLIST
######################################################################
@app.route('/wishlists', methods=['POST'])
def create_wishlist():
    """
    Creates an Wishlist object based on the JSON posted
    """
    check_content_type('application/json')
    wishlist = Wishlist()
    json_post = request.get_json()

    wishlist.deserialize(json_post)
    wishlist.save()
    message = wishlist.serialize()

    """
    Want to get the items from POST and create items associated
    with wishlist
    """
    current_wishlist_id = message['id']
    items = json_post['items']
    items_response = []
    for item_dict in items:
        item = Item()
        item.deserialize(item_dict, current_wishlist_id)
        item.save()
        items_response.append(item.serialize())
    """
    The individual responses during the loop were added to a list
    so that the responses can be added to the POST response
    """
    message['items'] = items_response

    location_url = url_for('get_wishlists', wishlist_id=wishlist.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                            'Location': location_url
                         })


######################################################################
# GET A WISHLIST
######################################################################
@app.route('/wishlists/<int:wishlist_id>', methods=['GET'])
def get_wishlists(wishlist_id):
    """
    Retrieve a single Wishlist

    This endpoint will return a Wishlist based on it's id
    """
    wishlist = Wishlist.get(wishlist_id)
    if not wishlist:
        raise NotFound("Wishlist with id '{}' was not found.".format(wishlist_id))
    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)


######################################################################
# LIST ALL WISHLISTS
######################################################################
@app.route('/wishlists', methods=['GET'])
def list_wishlists():
    """ Returns all of the Wishlists """
    wishlists = Wishlist.all()

    results = [wishlist.serialize() for wishlist in wishlists]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# DELETE A WISHLIST
######################################################################
@app.route('/wishlists/<int:wishlist_id>', methods=['DELETE'])
def delete_wishlist(wishlist_id):
    """
    Delete a Wishlist

    This endpoint will delete a Wishlist based on the id specified in
    the path
    """
    wishlist = Wishlist.get(wishlist_id)
    if wishlist:
        wishlist.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)



######################################################################
# DELETE AN ITEM FROM AN WISHLIST
######################################################################
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Delete an Item

    This endpoint will delete an Item based on the id specified in
    the path
    """
    item = Item.get(item_id)
    if item:
        item.delete()
    return make_response('', status.HTTP_204_NO_CONTENT) 

######################################################################
# UPDATE AN ITEM
######################################################################
@app.route('/wishlists/<int:wishlist_id>/items/<int:item_id>', methods=['PUT'])
def update_items(wishlist_id, item_id):
    """
    Update an Item

    This endpoint will update an Item based the body that is posted
    """
    check_content_type('application/json')
    item = Item.get(item_id)
    if not item:
        raise NotFound("Item with id '{}' was not found.".format(item_id))
    item.deserialize(request.get_json(), wishlist_id)
    item.id = item_id
    item.save()
    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# UTILITY FUNCTIONS
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    # Item.init_db(app)
    Wishlist.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))

def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')


######################################################################
# MAIN
######################################################################
if __name__ == "__main__":
    print "========================================="
    print " WISHLISTS  SERVICE STARTING"
    print "========================================="
    initialize_logging(logging.INFO)
    init_db()  # make our sqlalchemy tables
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)