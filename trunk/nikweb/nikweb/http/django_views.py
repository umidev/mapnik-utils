"""
Django view for nikweb.

* use settings.NIKWEB* to specify the settings:
    NIKWEB_MAP_DEFINITIONS:     local path to your map definitions (required)
    NIKWEB_MAP_LAYER_PREFIX:    layer prefix to use in the map XML files (optional; "NIKWEB")
    NIKWEB_DEFAULT_SIZE:        default map size tuple (optional; (512,512))

* set up the relevant parts of your urls.py like:
      (r'$',                   'nikweb.http.django_views.nikweb_index'),
      (r'(?P<map>[\w\.-]+)/$', 'nikweb.http.django_views.nikweb_render'),

"""
__all__ = ("nikweb_index", "nikweb_render")

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
try:
    import json
except ImportError:
    # Python <2.6 doesn't have a JSON module
    # Django has a copy
    from django.utils import simplejson as json

import nikweb.http

# global nikweb helper object
nikweb_http = nikweb.http.NikwebHttp(settings.NIKWEB_MAP_DEFINITIONS, 
                                     debug=settings.DEBUG, 
                                     map_layer_prefix=getattr(settings, 'NIKWEB_MAP_LAYER_PREFIX', None),
                                     default_size=getattr(settings, 'NIKWEB_DEFAULT_SIZE', None))

def nikweb_index(request):
    map_defs = nikweb_http.index()
    content = u"\n".join(map_defs) + u"\n"
    return HttpResponse(content, content_type='text/plain')
    
def nikweb_render(request, map):
    if request.method == 'POST':
        raw_data = request.raw_post_data
    elif 'q' in request.GET:
        raw_data = request.GET['q']
    else:
        return HttpResponseBadRequest("No 'q' parameter specified") 
    
    try:
        d = json.loads(raw_data.decode('utf-8'))
    except:
        return HttpResponseBadRequest('Error parsing JSON')

    try:
        image, content_type, elapsed = nikweb_http.render(map, d)
    except Exception, e:
        if settings.DEBUG:
            raise
        else:
            return HttpResponseServerError("Error rendering map")

    resp = HttpResponse(image, content_type=content_type)
    resp['X-nikweb-rendertime'] = "%0.3f" % elapsed
    return resp
    