var Tail = (function() {
    var cursor = null;
    var waitTime = 0;
    var cancel = false;
    var tailPath = null;
    var tailElt = null;
    var delimiter = new RegExp(' ');
    var numCells = null;
    var lastWasError = false;
    var currentRequest = null;
    
    var errback = function(xhr, textStatus, errorThrown) {
        if(cancel) {
            return;
        }
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
    
    var addShrinkRows = function(num) {
        var shrinkTable = $('<table id="shrink"></table>');
        var row = $('<tr></tr>');
        for(var i = 0; i < num; ++i) {
            (function() {
                var j = i;
                var td = $('<td><a href="#">&#x25C0;</a></td>');
                var grow = function() {
                    $('.col' + j).globalcss('max-width', 'inherit');
                    $('.col' + j).globalcss('opacity', '1');
                    $('.col' + j).globalcss('-moz-opacity', '1');
                    $('.col' + j).globalcss('-webkit-opacity', '1');
                    td.css('width', $($(tailElt + ' tr:last td')[j]).width());
                    $('a', td).html('&#x25C0;');
                    td.click(shrink);
                    return false;
                };
                var shrink = function() {
                    $('.col' + j).globalcss('max-width', '12px');
                    $('.col' + j).globalcss('opacity', '0.3');
                    $('.col' + j).globalcss('-moz-opacity', '0.3');
                    $('.col' + j).globalcss('-webkit-opacity', '0.3');
                    td.css('width', '12px');
                    $('a', td).html('&#x25BA;');
                    td.click(grow)
                    return false;
                };
                row.append(td.click(shrink).addClass('shrink' + j));
            })();
        }
        shrinkTable.append(row);
        $(tailElt).before($('<div id="shrink-container"></div>').append(shrinkTable));
        $(tailElt).scroll(function(e) {
            shrinkTable.css('margin-left', '-' + $(tailElt).scrollLeft() + 'px');
        });
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
                addShrinkRows(splitLine.length);
            }
            if(splitLine.length === numCells) {
                lastWasError = false;
                for(var j = 0; j < splitLine.length; ++j) {
                    var td = $('<td></td>').addClass('col' + j);
                    row.append(td.text(splitLine[j]));
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
        
        var latest = $(tailElt + ' tr:last td');
        for(var i = 0; i < latest.length; ++i) {
            var width = $(latest[i]).width();
            $('.shrink' + i).css('width', width).css('max-width', width);
        }
        $('#shrink').css('width', $(tailElt + ' tr:last').width());
        
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
            var height = $(window).height() - 260;
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
            if(currentRequest) {
                currentRequest.abort();
            }
            $('#start-tail').show();
            $('#stop-tail').hide();
        },
        
        tail: function() {
            var queryString = cursor ? {cursor: cursor} : {};
            currentRequest = $.ajax({
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