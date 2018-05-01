Feature: The wishlist service back-end
    As a cusomer
    I need a RESTful wishlist service
    So that I can keep track of all my wishlists and items within

Background: Data input
    Given the following wishlists
        | wishlist_id | wishlist_name| customer_id |
        |           1 | books        | 1           |
        |           2 | food         | 1           |
        |           3 | default      | 2           |        
    Given the following items
        | item_id | item_wishlist_id | item_product_id | item_name | item_description |
        | 1       | 1                | 1               | cs        | tdd              |
        | 2       | 1                | 2               | math      | algebra          |
        | 3       | 3                | 1               | cs        | bdd              |
        | 4       | 2                | 3               | burger    | vegetarian       |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlist RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Wishlist
    When I visit the "Home Page"
    And I set the "wishlist_name" to "test"
    And I set the "customer_id" to "1"
    And I press the "create" button
    Then I should see the message "Success"
	
Scenario: Get a Wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "1"
    And I press the "retrieve" button
    Then I should see "books" in the "wishlist_name" field
    And I should see "1" in the "customer_id" field  

Scenario: List all wishlists
    When I visit the "Home Page"
    And I press the "list" button
    Then I should see "books" in the wishlist results
    And I should see "food" in the wishlist results
    And I should see "default" in the wishlist results

Scenario: List all items in a specific wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "1"
    And I press the "list_item" button
    Then I should see "cs" in the item results
    And I should see "math" in the item results

Scenario: Delete a Wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "3"
    And I press the "delete" button
    Then I should see the message "Wishlist has been Deleted!"
    When I press the "list" button
    Then I should see "books" in the wishlist results
    And I should see "food" in the wishlist results
    And I should not see "default" in the wishlist results
    
Scenario: Clear a Wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "2"
    And I press the "clear-item" button
    Then I should see the message "Wishlist has its items cleared!"
    When I press the "list" button
    Then I should see "food" in the wishlist results
    When I press the "list_item" button
    Then I should not see "burger" in the item results

Scenario: Update a wishlist
    When I visit the "Home Page"
    And I set the "wishlist_id" to "1"
    And I press the "retrieve" button
    Then I should see "books" in the "wishlist_name" field
    When I change "wishlist_name" to "study"
    And I press the "update" button
    Then I should see the message "Success"
    When I press the "clear" button
    And I set the "wishlist_id" to "1"
    And I press the "retrieve" button
    Then I should see "study" in the "wishlist_name" field
    When I press the "clear" button
    And I press the "list" button
    Then I should see "study" in the wishlist results
    And I should not see "books" in the wishlist results

Scenario: Query a wishlist by its name
    When I visit the "Home Page"
    And I set the "wishlist_name" to "books"
    And I press the "search" button
    Then I should see "books" in the wishlist results
    And I should not see "food" in the wishlist results
    And I should not see "default" in the wishlist results

Scenario: Add an item 
    When I visit the "Home Page"
    And I set the "item_wishlist_id" to "1"
    And I set the "item_product_id" to "4"
    And I set the "item_name" to "flask"
    And I set the "item_description" to "web development"
    And I press the "add-item" button
    Then I should see the message "Success"
    When I press the "clear-it" button
    And I set the "wishlist_id" to "1"
    And I press the "list_item" button
    Then I should see "flask" in the item results

Scenario: Get an item 
    When I visit the "Home Page"
    And I set the "item_id" to "1"
    And I press the "retrieve-item" button
    Then I should see "1" in the "item_wishlist_id" field
    And I should see "1" in the "item_product_id" field
    And I should see "cs" in the "item_name" field
    And I should see "tdd" in the "item_description" field

Scenario: Delete an item
    When I visit the "Home Page"
    And I set the "item_id" to "3"
    And I set the "item_wishlist_id" to "3"
    And I press the "delete-thisitem" button
    Then I should see the message "Item has been Deleted!"
    When I press the "clear" button
    And I set the "wishlist_id" to "3"
    And I press the "list_item" button
    Then I should not see "cs" in the item results

Scenario: Update an item
    When I visit the "Home Page"
    And I set the "item_id" to "1"
    And I press the "retrieve-item" button
    Then I should see "1" in the "item_wishlist_id" field
    And I should see "1" in the "item_product_id" field
    And I should see "cs" in the "item_name" field
    And I should see "tdd" in the "item_description" field
    When I change "item_description" to "devops"
    And I press the "update-item" button
    Then I should see the message "Success"
    When I press the "clear-it" button
    And I change "item_id" to "1"
    And I press the "retrieve-item" button
    Then I should see "devops" in the "item_description" field
    






