var Tail = (function() {
    var cursor = null;
    var waitTime = 0;
    var cancel = false;
    var tailPath = null;
    var tailElt = null;
    
    var errback = function(xhr, textStatus, errorThrown) {
        if(waitTime === 0) {
            waitTime = 60;
        }
        else {
            waitTime *= 2;
        }
        setTimeout(function(){ tail(path, tailElt ); }, waitTime);
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
            $('<li></li>').text(data.lines[i]).appendTo(tailElt);
        }
        while($(tailElt + ' li').length > 100) {
            $(tailElt + ' li:first').remove();
        }
        /* The 9999 here is a hack */
        $(tailElt).animate({scrollTop: 9999}, 100);
        if(!cancel) {
            Tail.tail(tailPath, tailElt);
        }
    };
    
    return {
        setup: function(path, elt) {
            tailPath = path;
            tailElt = elt;
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