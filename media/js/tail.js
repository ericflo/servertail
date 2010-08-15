var Tail = (function() {
    var cursor = null;
    var waitTime = 0;
    var cancel = false;
    var tailPath = null;
    var tailElt = null;
    var delimiter = new RegExp(' ');
    var numCells = null;
    var lastWasError = false;
    
    var errback = function(xhr, textStatus, errorThrown) {
        $('#waiting-help').show();
        $(tailElt).hide();
        if(waitTime === 0) {
            waitTime = 60;
        }
        else {
            waitTime *= 1.2;
        }
        setTimeout(function(){ Tail.tail(tailPath, tailElt ); }, waitTime);
    };
    
    var callback = function(data) {
        /* If the server hangs up on a long poll, it won't go to errback, so
           we need for force it to do so. */
        if(!data) {
            return errback();
        }
        
        if(data.error) {
            return errback();
        }
        
        $('#waiting-help').hide();
        $(tailElt).show();
        
        /* Detect if they're scrolled to the bottom */
        var elem = $(tailElt);
        var scrollHeight = elem[0].scrollHeight;
        var atBottom = Math.abs((scrollHeight - elem.scrollTop()) -
            elem.outerHeight()) < 20;
        
        waitTime = 0;
        cursor = data.cursor;
        for(var i = 0; i < data.lines.length; ++i) {
            var row = $('<tr></tr>');
            var splitLine = data.lines[i].split(delimiter);
            if(numCells === null) {
                numCells = splitLine.length;
            }
            if(splitLine.length === numCells) {
                lastWasError = false;
                for(var j = 0; j < splitLine.length; ++j) {
                    row.append($('<td></td>').text(splitLine[j]));
                }
                row.appendTo(tailElt);
            }
            else {
                if(lastWasError) {
                    var pre = $('<pre></pre>').text(data.lines[i]);
                    $(tailElt + ' tr:last td').append(pre);
                }
                else {
                    lastWasError = true;
                    var cell = $('<td></td>').attr('colspan', numCells);
                    cell = cell.html($('<pre></pre>').text(data.lines[i]));
                    row.addClass('error').append(cell).appendTo(tailElt);
                }
            }
        }
        
        if(atBottom) {
            while($(tailElt + ' tr').length > 100) {
                $(tailElt + ' tr:first').remove();
            }
            $(tailElt).scrollTop(9999);
        }
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
            var height = $(window).height() - 240;
            $(elt).css('height', height);
            $('#waiting-help').css('height', height);
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
                timeout: 10000,
                data: queryString,
                dataType: 'json',
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