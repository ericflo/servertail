import simplejson
 
from django.http import HttpResponse
from django.conf import settings
 
class JSONResponse(HttpResponse):
    def __init__(self, data):
        indent = 2 if settings.DEBUG else None
        mime = "text/javascript" if settings.DEBUG else "application/json"
        super(JSONResponse, self).__init__(
            content = simplejson.dumps(data, indent=indent),
            mimetype = mime,
        )