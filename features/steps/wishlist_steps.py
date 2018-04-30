"""
Wishlist Steps
Steps file for Wishlists.feature
"""
from os import getenv
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import server

WAIT_SECONDS = 30
BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@given(u'the following wishlists')
def step_impl(context):
    """ Delete all wishlists and item and load new wishlists """
    headers = {'Content-Type': 'application/json'}
    #bad code here, or we need to write a reset method for wishlists
    for i in range(4):
    	context.resp = requests.delete(context.base_url + '/wishlists/'+str(i), headers=headers)
    	expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/wishlists'
    for row in context.table:
        data = {
            "id": row['wishlist_id'],
            "customer_id": row['customer_id'],
            "wishlist_name": row['wishlist_name']
            }	
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)


@given(u'the following items')
def step_impl(context):
    """ load new items deleted by given wishlists """
    headers = {'Content-Type': 'application/json'}
    #context.resp = requests.delete(context.base_url + '/wishlists/reset', headers=headers)
    #expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/wishlists/'
    for row in context.table:
        data = {
            "wishlist_id": row['item_wishlist_id'],
            "product_id": row['item_product_id'],
            "name": row['item_name'],
            "description":row['item_description']
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url+ '/' + row['wishlist_id']+'/items', data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)

@when(u'I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
    #context.driver.save_screenshot('home_page.png')

@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)


@then(u'I should see the message "{message}"')
def step_impl(context, message):
    #element = context.driver.find_element_by_id('flash_message')
    #expect(element.text).to_contain(message)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)

@then(u'I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@when(u'I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clear button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################

@when(u'I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@then(u'I should see "{name}" in the wishlist results')
def step_impl(context, name):
    #element = context.driver.find_element_by_id('search_results')
    #expect(element.text).to_contain(name)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'wishlist_results'),
            name
        )
    )
    expect(found).to_be(True)

@then(u'I should see "{name}" in the item results')
def step_impl(context, name):
    #element = context.driver.find_element_by_id('search_results')
    #expect(element.text).to_contain(name)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'item_results'),
            name
        )
    )
    expect(found).to_be(True)

@then(u'I should not see "{name}" in the wishlist results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('wishlist_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)


@then(u'I should not see "{name}" in the item results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('item_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)


@then(u'I should see "{message}" in the "{field}" field')
def step_impl(context, message, field):
    """ Check a field for text """
    element = context.driver.find_element_by_id(field)
    assert message in element.text
