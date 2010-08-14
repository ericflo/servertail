from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from tail.models import ServerTail

def tail(request, tail_id=None):
    server_tail = get_object_or_404(ServerTail, id=tail_id)
    context = {
        'server_tail': server_tail,
    }
    return render_to_response('tail/tail.html', context,
        context_instance=RequestContext(request))