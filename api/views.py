#import json
# from django.http import JsonResponse --> intially used
# from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from products.serializers import ProductSerializer
# Create your views here.


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addProduct(request):
    # DRF API VIEW
    data = {}
    serializer = ProductSerializer(data=request.data)
    # raise exception will catch an invalid error and throw it.
    if serializer.is_valid(raise_exception=True):
        # creating an instance from the serializer, has something to do with database
        # if we save the serializer we do not need the try catch block in the serializer for get_my_discount
        instance = serializer.save()
        print(serializer.data)
        # data = serializer.data
        print(instance)
        return Response(serializer.data)
    return Response({"Error": "Not good"}, status=400)


@api_view(["GET"])
def getAllProducts(request):
    # DRF API VIEW
    instance = Product.objects.all().order_by("?")
    data = {}
    if instance:
        data = ProductSerializer(instance, many=True).data
    return Response(data)

    # Starting things(not useful with drf)
    # request -> httpreq
    # request.body --> data from the frontend coming in.
    # body = request.body  # byte string of JSON data
    # data = {}
    # try:
    #     data = json.loads(body)  # string of json data to a dictionary
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

    # Django model instance as api response(working with models without drf)
    # model_data = Product.objects.all().order_by("?").first()
    # data = {}
    # if model_data:
    #     data = model_to_dict(model_data, fields=['id', 'title'])
    # process of serialization
    # we basically have a model instance (model_data)
    # then we turn it into a python dict and
    # return json to client
    # jsonresponse accepts a dictionary as an argument
    # without using model_to_dict, we can also do it like this
    # data['id'] = model_data.id
    # data['title'] = model_data.title
    # data['content'] = model_data.content
    # data['price'] = model_data.price
    # return JsonResponse(data)
