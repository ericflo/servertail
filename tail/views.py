import time
import uuid

from collections import defaultdict

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

import eventlet
from eventlet import event

from tail.models import ServerTail

def tail(request, tail_id=None):
    server_tail = get_object_or_404(ServerTail, id=tail_id)
    context = {
        'server_tail': server_tail,
    }
    return render_to_response('tail/tail.html', context,
        context_instance=RequestContext(request))


class DataCollectionView(object):
    
    def __init__(self, idle_time=60*5):
        self.data = defaultdict(lambda: [])
        self.greenlets = {}
        self.events = defaultdict(lambda: [])
        self.idle_time = idle_time
    
    def view(self, request, tail_id=None):
        tail_id = int(tail_id)
        greenlet = self.greenlets.get(tail_id)
        if not greenlet:
            server_tail = get_object_or_404(ServerTail, id=tail_id)
            self.greenlets[tail_id] = eventlet.spawn(self.data_getter, tail)
        data_event = event.Event()
        self.events[tail_id].append(data_event)
        data_event.wait()
        
        cursor = request.GET.get('cursor')
        if cursor:
            # There's gotta be a more elegant way to write this
            lines = []
            seen_cursor = False
            for line in self.data[tail_id]:
                if seen_cursor:
                    lines.append(line)
                elif line['id'] == cursor:
                    seen_cursor = True
            # Their cursor could just have been way too far back
            if not lines:
                lines = self.data[tail_id]
        else:
            lines = self.data[tail_id]
        
        new_cursor = lines[-1]['id'] if lines else None
        
        return JSONResponse({
            'cursor': new_cursor,
            'lines': lines_to_send,
        })
    
    def data_getter(self, tail_id):
        pass