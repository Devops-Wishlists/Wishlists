Feature: The wishlist service back-end
    As a cusomer
    I need a RESTful wishlist service
    So that I can keep track of all my wishlists and items within

Background:
    Given the following wishlists
        | wishlist_id | wishlist_name| customer_id |
        |           1 | books        | 1           |
        |           2 | food         | 1           |
        |           3 | default      | 2           |

    Given the following items
        |item_id | wishlist_id | product_id | name   | description |
        | 1      |           1 |         1  | cs     | tdd         |
        | 2      |           1 |         2  | math   | algebra     |
        | 3      |           3 |         1  | cs     | bdd         |
        | 4      |           2 |         3  | burger | vegetarian  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlist RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Wishlist
    When I visit the "Home Page"
    And I set the "wishlist_name" to "test"
    And I set the "customer_id" to "1"
    And I press the "Create" button
    Then I should see the message "Success"
    When I press "List_wishlist" button
    Then I should see "test" in the results

Scenario: Get a Wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "1"
    And I press the "Retrieve_wishlist" button
    Then I should see "books" in the "name" field
    And I should see "1" in the "customer_id" field  

Scenario: List all wishlists
    When I visit the "Home Page"
    And I press the "List_wishlist" button
    Then I should see "books" in the results
    And I should see "food" in the results
    And I should see "default" in the results

Scenario: List all items in a specific wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "1"
    And I press the "List_item" button
    Then I should see "cs" in the results
    And I should see "math" in the results

Scenario: List all items in the system
    When I visit the "Home Page"
    And I press the "List_item" button
    Then I should see "cs" in the results
    And I should see "math" in the results
    And I should see "burger" in the results

Scenario: Delete a Wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "2"
    And I press the "Delete_wishlist" button
    Then I should see "Success" in the results
    When I press the "List_wishlist" button
    Then I should not see "food" in the results
    When I press the "List_item" button
    Then I should not see "burger" in the results

Scenario: Clear a Wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "2"
    And I press the "Clear_wishlist"
    Then I should see "Success" in the results
    When I press the "List_wishlist" button
    Then I should see "food" in the results
    When I press the "List_item" button
    Then I should not see "burger" in the results

Scenario: Update a wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "1"
    And I press the "Retrieve_wishlist" button
    Then I should see "books" in the "name" field
    When I change "books" to "textbooks"
    And I press the "Update_wishlist" button
    Then I should see the message "Success"
    When I press the "clear_wishlist_fields" button
    And I set "wishlist_id" to "1"
    And I press the "Retrieve_wishlist" button
    Then I should see "textbooks" in the "name" field
    When I press the "Clear_wishlist_fields" button
    And I press the "List_wishlist" button
    Then I should see "textbooks" in the results
    And I should not see "books" in the results

Scenario: Query a wishlist by its name
    When I visit the "Home Page"
    And I set the "wishlist_name" to "books"
    And I press the "Search" button
    Then I should see "books" in the results
    And I should not see "food" in the results
    And I should not see "default" in the results

Scenario: Add an item 
    When I visit the "Home Page"
    And I set the "wishlist_id" to "1"
    And I set the "product_id" to "4"
    And I set the "item_name" to "flask"
    And I set the "description" to "web development"
    And I press the "Add_to_wishlist" button
    Then I should "Success" in the results
    When I press "Clear_wishlist_fields" button
    And  I press "List_item" button
    Then I should see "flask" in the results
    When I set "wishlist_id" to "1"
    And I press "List_item" button
    Then I should see "flask" in the results

Scenario: Get an item 
    When I visit the "Home Page"
    And I set the "item_id" to "1"
    And I press the "Retrieve_item" button
    Then I should see "1" in the "wishlist_id" field
    And I should see "1" in the "product_id" field
    And I should see "cs" in the "name" field
    And I should see "tdd" in the "description" field

Scenario: Delete an item
    When I visit the "Home Page"
    And I set the "item_id" to "3"
    And I press the "Delete_item" button
    Then I should see "Success" in the results
    When I press "clear_wishlist_fields" button
    And I set "wishlist_id" to "3"
    And I press the "Retrieve_item" button
    Then I should not see "cs" in the results
    When I press "clear_wishlist_fields" button
    And I press the "List_wishlist" button
    Then I should not see "cs" in the results

Scenario: Update an item
    When I visit the "Home Page"
    And I set the "item_id" to "1"
    And I press the "Retrieve_item" button
    Then I should see "1" in the "item_wishlist_id" field
    And I should see "1" in the "item_product_id" field
    And I should see "cs" in the "item_name" field
    And I should see "tdd" in the "item_description" field
    When I change "tdd" to "devops"
    And I press the "Update_item" button
    Then I should see the message "Success"
    When I press the "Clear_item_fields" button
    And I set the "item_id" to "1"
    And I press the "Retrieve_item" button
    Then I should see "devops" in the "item_description" field
    







