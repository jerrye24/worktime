$('#id_employee_label').autocomplete({
    minLength: 2,
    source: function (request, response) {
        $.ajax({
            url: "/tabel_json/",
            dataType: "json",
            data: {term: request.term},
            success: function(data) {response(data)}
        })
    },
    select: function (event, ui) {
        $(this).val(ui.item.value);
        $('#id_employee').val(ui.item.id)
    }
});