import operator
import os
import uuid

from collections import defaultdict

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django_ext.http import JSONResponse

import eventlet
from eventlet import event

import paramiko

from tail.models import ServerTail

def tail(request, tail_id=None):
    server_tail = get_object_or_404(ServerTail, id=tail_id)
    context = {
        'server_tail': server_tail,
    }
    return render_to_response('tail/tail.html', context,
        context_instance=RequestContext(request))


class DataCollectionView(object):
    
    def __init__(self, idle_time=60*5, buffer_limit=100):
        self.data = defaultdict(lambda: [])
        self.greenlets = {}
        self.events = defaultdict(lambda: [])
        self.idle_time = idle_time
        self.buffer_limit = buffer_limit
    
    def _get_latest_lines(self, tail_id, cursor):
        # There's gotta be a more elegant way to write this
        if not cursor:
            return self.data[tail_id]
        lines = []
        seen_cursor = False
        for line in self.data[tail_id]:
            if seen_cursor:
                lines.append(line)
            elif line['id'] == cursor:
                seen_cursor = True
        return lines
    
    def view(self, request, tail_id=None):
        tail_id = int(tail_id)
        
        greenlet = self.greenlets.get(tail_id)
        if not greenlet:
            server_tail = get_object_or_404(ServerTail, id=tail_id)
            self.greenlets[tail_id] = eventlet.spawn(self.data_getter,
                server_tail)
        
        cursor = request.GET.get('cursor')
        
        lines = self._get_latest_lines(tail_id, cursor)
        
        if not lines:
            data_event = event.Event()
            self.events[tail_id].append(data_event)
            resp = data_event.wait()
            if resp['error']:
                return JSONResponse({'error': True},
                    request.GET.get('callback'))
            lines = self._get_latest_lines(tail_id, cursor)
    
        # Their cursor could just have been way too far back
        #if not lines:
        #    lines = self.data[tail_id]
        
        new_cursor = lines[-1]['id'] if lines else None
        
        lines = map(operator.itemgetter('line'), lines)
        
        return JSONResponse({
            'cursor': new_cursor,
            'lines': lines,
        }, request.GET.get('callback'))
    
    def _data_getter(self, server_tail):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        kwargs = {}
        if server_tail.username:
            kwargs['username'] = server_tail.username
        if server_tail.password:
            kwargs['password'] = server_tail.password
        rsa_key = '/home/servertail/.ssh/id_rsa'
        if os.path.exists(rsa_key):
            kwargs['key_filename'] = rsa_key
        client.connect(server_tail.hostname, server_tail.port, **kwargs)
        
        command = 'uname -a'
        stdin, stdout, stderr = client.exec_command(command)
        if 'Darwin' in stdout.read():
            command = 'tail -n%s -F %s' % (self.buffer_limit, server_tail.path)
        else:
            command = 'tail -q -s0.08 -n%s -F %s 2>&1' % (self.buffer_limit,
                server_tail.path)
        
        stdin, stdout, stderr = client.exec_command(command)
                
        for line in stdout:
            line_id = str(uuid.uuid1())
            self.data[server_tail.id].append({
                'id': line_id,
                'line': line.strip(),
            })
            truncated = self.data[server_tail.id][-self.buffer_limit:]
            self.data[server_tail.id] = truncated
            events = self.events.pop(server_tail.id, [])
            for event in events:
                event.send({'error': False, 'id': line_id})
    
    def data_getter(self, server_tail):
        try:
            return self._data_getter(server_tail)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            events = self.events.pop(server_tail.id, [])
            for event in events:
                event.send({'error': True})

data = DataCollectionView().view