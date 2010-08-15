$(function() {
    /* Add the change handler on the tail jump list */
    var tailJumpList = $('#quickjump');
    if(tailJumpList.length) {
        var tailJumpListSelect = $('select', tailJumpList);
        tailJumpListSelect.change(function(e) {
            document.location = tailJumpListSelect.val();
        });
    }
});