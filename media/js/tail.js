var cursor = null;
var waitTime = 0;

function tail(path, elt) {
    var errback = function(xhr, textStatus, errorThrown) {
        if(waitTime === 0) {
            waitTime = 60;
        }
        else {
            waitTime *= 2;
        }
        setTimeout(function(){ tail(path, elt ); }, waitTime);
    };
    var callback = function(data) {
        /* If the server hangs up on a long poll, it won't go to errback, so
           we need for force it to do so. */
        if(!data) {
            return errback();
        }
        waitTime = 0;
        cursor = data.cursor;
        for(var i = 0; i < data.lines.length; ++i) {
            $('<li></li>').text(data.lines[i]).appendTo(elt);
        }
        while($(elt + ' li').length > 100) {
            $(elt + ' li:first').remove();
        }
        /* The 9999 here is a hack */
        $(elt).animate({scrollTop: 9999}, 100);
        tail(path, elt);
    };
    var queryString = cursor ? {cursor: cursor} : {};
    $.ajax({
        url: path,
        data: queryString,
        dataType: 'jsonp',
        success: callback,
        error: errback
    });
}