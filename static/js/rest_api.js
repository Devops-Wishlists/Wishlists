$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#wishlist_id").val(res.id);
        $("#customer_id").val(res.customer_id);
        $("#wishlist_name").val(res.wishlist_name);
    }

    function update_itemform_data(res) {
        $("#item_id").val(res.id);        
        $("#item_wishlist_id").val(res.wishlist_id);
        $("#item_product_id").val(res.product_id);
        $("#item_name").val(res.name);
        $("#item_description").val(res.description);
    }

    /// Clears all form fields
    function clear_form_data() { 
        $("#wishlist_name").val("");
        $("#customer_id").val("");
    }

    function clear_item_form_data() {
        $("#item_product_id").val("");
        $("#item_wishlist_id").val("");
        $("#item_name").val("");
        $("#item_description").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create-btn").click(function () {

        var customer_id = $("#customer_id").val();
        var wishlist_name = $("#wishlist_name").val();

        var data = {
            "customer_id": customer_id,
            "wishlist_name": wishlist_name,
        };

        console.log(JSON.stringify(data));

        var ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Wishlist
    // ****************************************

    $("#update-btn").click(function () {

        var wishlist_id = $("#wishlist_id").val();
        var wishlist_name = $("#wishlist_name").val();
        var customer_id = $("#customer_id").val();

        var data = {
            "wishlist_id": wishlist_id,
            "wishlist_name": wishlist_name,
            "customer_id": customer_id
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/wishlists/" + wishlist_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {

        var wishlist_id = $("#wishlist_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists/" + wishlist_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#delete-btn").click(function () {

        var wishlist_id = $("#wishlist_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/wishlists/" + wishlist_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        clear_form_data();
    });

    // ****************************************
    // Clear the wishlist
    // ****************************************

    $("#clear-item-btn").click(function () {
        var wishlist_id = $("#wishlist_id").val();
        
        var ajax = $.ajax({
            type: "PUT",
            url: "/wishlists/" + wishlist_id + "/clear",
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist has its items cleared!")
        });

        ajax.fail(function(res){
            flash_message("Server error! Couldn't clear wishlist!")
        });

    });

    // ****************************************
    // List all Wishlists
    // ****************************************

    $("#list-btn").click(function () {

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists",
            contentType:"application/json"
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#wishlist_results").empty();
            $("#wishlist_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:40%">ID</th>'
            header += '<th style="width:40%">Customer ID</th>'
            header += '<th style="width:40%">Wishlist Name</th>'
            $("#wishlist_results").append(header);
            for(var i = 0; i < res.length; i++) {
                wishlist = res[i];
                var row = "<tr><td>"+wishlist.id+"</td><td>"+wishlist.customer_id+"</td><td>"+wishlist.wishlist_name+"</td></tr>";
                $("#wishlist_results").append(row);
            }

            $("#wishlist_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // List Items from a Wishlist
    // ****************************************

    $("#list_item-btn").click(function () {
        
        var wishlist_id = $("#wishlist_id").val();
        var url = "/wishlists/"+ wishlist_id+ "/items";
        
        console.log(url);

        var ajax = $.ajax({
            type: "GET",
            url: url,
            contentType:"application/json"
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#item_results").empty();
            $("#item_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">Wishlist ID</th>'
            header += '<th style="width:10%">Product ID</th>'
            header += '<th style="width:20%">Name</th>'
            header += '<th style="width:40%">Description</th></tr>'
            $("#item_results").append(header);
            for(var i = 0; i < res.length; i++) {
                item = res[i];
                var row = "<tr><td>"+item.wishlist_id+"</td><td>"+item.product_id+"</td><td>"+item.name+"</td><td>"+item.description+"</td></tr>";
                $("#item_results").append(row);
            }

            $("#item_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Add an Item to a Wishlist
    // ****************************************

    $("#add-item-btn").click(function () {

        var product_id = $("#item_product_id").val();
        var name = $("#item_name").val();
        var description = $("#item_description").val();
        var wishlist_id = $("#item_wishlist_id").val();

        var data = {
            "product_id": product_id,
            "name": name,
            "description": description
        };

        console.log(data);

        var ajax = $.ajax({
            type: "POST",
            url: "/wishlists/" + wishlist_id +"/items",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_itemform_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Clear the item form
    // ****************************************

    $("#clear-it-btn").click(function () {
        clear_item_form_data();
    });

    // ****************************************
    // Update an Item
    // ****************************************

    $("#update-item-btn").click(function () {

        var item_id = $("#item_id").val();
        var wishlist_id = $("#item_wishlist_id").val();
        var product_id = $("#item_product_id").val();
        var name = $("#item_name").val();
        var description = $("#item_description").val();

        var data = {
            "product_id": product_id,
            "name": name,
            "description": description,
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/wishlists/" + wishlist_id + "/items/" + item_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_itemform_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Item
    // ****************************************

    $("#retrieve-item-btn").click(function () {

        var item_id = $("#item_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/items/" + item_id,
            contentType:"application/json"
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_itemform_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_item_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an Item
    // ****************************************

    $("#delete-thisitem-btn").click(function () {

        var item_id = $("#item_id").val();
        var wishlist_id = $("#item_wishlist_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/wishlists/" + wishlist_id + "/items/" + item_id,
            contentType:"application/json"
        })

        ajax.done(function(res){
            clear_item_form_data()
            flash_message("Item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Search for a Wishlist
    // ****************************************
    $("#search-btn").click(function () {

        var customer_id = $("#customer_id").val();
        var wishlist_name = $("#wishlist_name").val();

        var data = {
            "customer_id": customer_id,
            "wishlist_name": wishlist_name,
        };

        console.log(JSON.stringify(data));

        var keyword = ""

        if (wishlist_name) {
            keyword += 'keyword=' + wishlist_name
            var url = "/wishlists?" + keyword
        }

        if (customer_id){
            customer_id += 'customer_id=' + customer_id
            var url = "/wishlists?" + customer_id
        }
        
        var ajax = $.ajax({
            type: "GET",
            url: url,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#wishlist_results").empty();
            $("#wishlist_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:40%">ID</th>'
            header += '<th style="width:40%">Customer ID</th>'
            header += '<th style="width:40%">Wishlist Name</th>'
            $("#wishlist_results").append(header);
            for(var i = 0; i < res.length; i++) {
                wishlist = res[i];
                var row = "<tr><td>"+wishlist.id+"</td><td>"+wishlist.customer_id+"</td><td>"+wishlist.wishlist_name+"</td></tr>";
                $("#wishlist_results").append(row);
            }

            $("#wishlist_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });
})
