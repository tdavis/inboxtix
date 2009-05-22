from django.http import HttpResponse, HttpResponseForbidden
from django.core.cache import cache
from inboxtix.util import get_api_tree


def autocomplete_category(request):
    if not request.is_ajax():
        return HttpResponseForbidden()
    name = request.GET.get('q',None)
    limit = request.GET.get('limit', 10)
    if not name:
        return HttpResponse('')
    tree = get_api_tree('category', 'search', **{'name':name, 'limit':limit})
    matches = []
    for cat in tree.iter('category'):
        matches.append(cat.find('name').text)

    return HttpResponse('\n'.join(matches))

