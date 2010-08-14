var Tail = (function() {
    var cursor = null;
    var waitTime = 0;
    var cancel = false;
    var tailPath = null;
    var tailElt = null;
    var delimiter = new RegExp(' ');
    
    var errback = function(xhr, textStatus, errorThrown) {
        if(waitTime === 0) {
            waitTime = 60;
        }
        else {
            waitTime *= 2;
        }
        setTimeout(function(){ Tail.tail(tailPath, tailElt ); }, waitTime);
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
            var row = $('<tr></tr>');
            var splitLine = data.lines[i].split(delimiter);
            for(var j = 0; j < splitLine.length; ++j) {
                $('<td></td>').text(splitLine[j]).appendTo(row);
            }
            row.appendTo(tailElt);
        }
        while($(tailElt + ' tr').length > 100) {
            $(tailElt + ' tr:first').remove();
        }
        /* The 9999 here is a hack */
        $(tailElt).animate({scrollTop: 9999}, 100);
        if(!cancel) {
            Tail.tail(tailPath, tailElt);
        }
    };
    
    return {
        setup: function(path, elt, delim) {
            tailPath = path;
            tailElt = elt;
            if(delim) {
                delimiter = delim;
            }
        },
        
        start: function() {
            cancel = false;
            $('#start-tail').hide();
            $('#stop-tail').show();
            Tail.tail();
        },
        
        stop: function() {
            cancel = true;
            $('#start-tail').show();
            $('#stop-tail').hide();
        },
        
        tail: function() {
            var queryString = cursor ? {cursor: cursor} : {};
            $.ajax({
                url: tailPath,
                data: queryString,
                dataType: 'jsonp',
                success: callback,
                error: errback
            });
        }
    };
})();

$(function() {
    $('#start-tail').click(function() {
        Tail.start();
        return false;
    });
    $('#stop-tail').click(function() {
        Tail.stop();
        return false;
    });
});