$('.tablesorter').tablesorter();
$('th')
    .mouseenter(function () {
        $(this).addClass('text-info')
    })
    .mouseleave(function () {
        $(this).removeClass('text-info')
    });
