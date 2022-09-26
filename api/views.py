#import json
#from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer
# Create your views here.


@api_view(["GET"])
def index(request):
    # DRF API VIEW
    instance = Product.objects.all().order_by("?").first()
    data = {}
    if instance:
        # data = model_to_dict(model_data, fields=['id', 'title'])
        data = ProductSerializer(instance).data
    return Response(data)
    # request -> httpreq
    # request.body
    # body = request.body  # byte string of JSON data
    # data = {}
    # try:
    #     data = json.loads(body)  # string of json data -> dictionary
    # except:
    #     pass
    # print(data)
    # # can also add to the data
    # # without dict(), request.headers is not json serializable
    # data['headers'] = dict(request.headers)
    # data['content_type'] = request.content_type
    # # handling query params
    # print(request.GET)  # gets query params
    # data['params'] = dict(request.GET)
    # model_data = Product.objects.all().order_by("?").first()
    # data = {}
    # if model_data:
    #     data = model_to_dict(model_data, fields=['id', 'title'])
    # process of serialization
    # model instance (model_data)
    # turn it into a python dict
    # return json to client
    # jsonresponse accepts a dictionary as an argument
    # data['id'] = model_data.id
    # data['title'] = model_data.title
    # data['content'] = model_data.content
    # data['price'] = model_data.price
    # another way to do all of the above
    # return Response(data)
