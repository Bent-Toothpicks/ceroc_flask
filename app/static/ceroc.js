$(function () {
    $("#person").autocomplete({
        source: function (request, response) {
            $.getJSON("personcomplete", {
                q: request.term, // in flask, "q" will be the argument to look for using request.args
            }, function (data) {
                response(data.matching_results); // matching_results from jsonify
            });
        },
        classes: {"ui-autocomplete" :"highlight", "ui-dialog-content": "modal-body"},
        minLength: 1,
        select: function (event, ui) {
            console.log(ui.item.value); // not in your question, but might help later
        }
    }).focus(function () {
        $(this).autocomplete('search')
    });

    $("#person").addClass(".ui-autocomplete");

    $("#event_id").change(function (e) {
        e.preventDefault();
        var value = $("#event_id").val();
        $.ajax({
            type: "GET",
            url: "event_data",
            data: { 'q': value } //JSON.stringify({ "text" : value } ),
            //            contentType: "application/json; charset=utf-8",
            //            dataType: "json" //,
            //          success: function (data) {
            //                alert(JSON.stringify(data));
            //            }
        });
    });

    $("#regotable, #eventstable").DataTable();

    // $("#regotable tbody").addClass("table-body scroll-tbody-y");
    // $("#eventstable tbody").addClass("table-body scroll-tbody-y");
})


$(function () {
    $("#sales_type").change(function () {
        console.log($("#sales_type").find(":selected").text())
        console.log($("#person").find(":selected").val())
        console.log($("#person").val())

    })
})