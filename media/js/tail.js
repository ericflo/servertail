var cursor = null;

function tail(path, elt) {
    var queryString = cursor ? {cursor: cursor} : {};
    $.getJSON(path, queryString, function(data) {
        cursor = data.cursor;
        for(var i = 0; i < data.lines.length; ++i) {
            console.log(data.lines[i].line);
            $('<li></li>').text(data.lines[i].line).appendTo(container);
        }
        $('html, body').animate({scrollTop: $(container).height()}, 100);
        tail(path, elt);
    });
}