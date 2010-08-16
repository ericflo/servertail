$(function() {
    /* Add the change handler on the tail jump list */
    var tailJumpList = $('#quickjump');
    if(tailJumpList.length) {
        var tailJumpListSelect = $('select', tailJumpList);
        tailJumpListSelect.change(function(e) {
            var target = tailJumpListSelect.val();
            if(target && target[0] === '/') {
                document.location = target;
            }
        });
    }
    
    /* Add lightbox intercepter */
    $('a.tail-create').colorbox({
        transition: 'none',
        width: 400,
        height: 520,
        iframe: true
    });
});