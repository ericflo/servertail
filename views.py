from django.shortcuts import render_to_response
from django.template import RequestContext

from tail.models import FrontPage

def index(request):
    try:
        server_tail = FrontPage.objects.order_by('-date')[0].server_tail
    except IndexError:
        server_tail = None
    context = {
        'server_tail': server_tail,
    }
    return render_to_response('index.html', context,
        context_instance=RequestContext(request))