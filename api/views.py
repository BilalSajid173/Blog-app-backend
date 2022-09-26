from django.http import JsonResponse
import json
# Create your views here.


def index(request):
    # request -> httpreq
    # request.body
    body = request.body  # byte string of JSON data
    data = {}
    try:
        data = json.loads(body)  # string of json data -> dictionary
    except:
        pass
    print(data)
    # can also add to the data
    # without dict(), request.headers is not json serializable
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    # handling query params
    print(request.GET)  # gets query params
    data['params'] = dict(request.GET)
    return JsonResponse({"message": "Hi There!!"})
