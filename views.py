from django.shortcuts import render_to_response
from django.template import RequestContext

from tail.models import FrontPage
from tail.utils import get_public_key

def index(request):
    try:
        server_tail = FrontPage.objects.order_by('-date')[0].server_tail
    except IndexError:
        server_tail = None
    context = {
        'server_tail': server_tail,
        'public_key': get_public_key(),
        'index': True,
    }
    return render_to_response('index.html', context,
        context_instance=RequestContext(request))