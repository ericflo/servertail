$(function() {
    /* Add the change handler on the tail jump list */
    var tailJumpList = $('#quickjump');
    if(tailJumpList.length) {
        var tailJumpListSelect = $('select', tailJumpList);
        tailJumpListSelect.change(function(e) {
            document.location = tailJumpListSelect.val();
        });
    }
    
    /* Add lightbox intercepter */
    $('a.tail-create').colorbox({
        transition: 'none',
        width: 400,
        height: 600,
        iframe: true
    });
});