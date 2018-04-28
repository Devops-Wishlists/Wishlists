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

    /// Clears all form fields
    function clear_form_data() {
        $("#wishlist_name").val("");
        $("#wishlist_id").val("");
        $("customer_id").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************
/*
    $("#create-btn").click(function () {

        var id = $("#customer_id").val();
        var name = $("#wishlist_name").val();

        var data = {
            "customer_id": id,
            "name": name,
        };

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
*/

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
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist with ID [" + res.id + "] has been Deleted!")
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

    $("clear-wishlist-btn").click(function () {
        var ajax = $.ajax({
            type: "PUT",
            url: "/wishlists/" + wishlist_id + "/clear",
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist with ID [" + res.id + "] has its items cleared!")
        });

        ajax.fail(function(res){
            flash_message("Server error! Couldn't clear wishlist!")
        });
    });

    // ****************************************
    // Search for a Wishlist
    // ****************************************
/*
    $("#search-btn").click(function () {

        var name = $("#wishlist_name").val();
        var category = $("#wishlist_category").val();
        var available = $("#wishlist_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                wishlist = res[i];
                var row = "<tr><td>"+wishlist.id+"</td><td>"+wishlist.name+"</td><td>"+wishlist.category+"</td><td>"+wishlist.available+"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });
*/
})
