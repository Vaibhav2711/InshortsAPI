from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import Serializer
from snippets.inshorts import getNews 
from django.http import JsonResponse
import json
@api_view(['GET', 'POST'])
def snippet_list(request, format = None):
    if request.method == 'GET':
        try:
          return JsonResponse(getNews(request.GET.get('category','')))
        except Exception as e:
          print(JsonResponse("Bad request",safe = False))

    elif request.method == 'POST':
        try:
          return JsonResponse(getNews(request.data['category']))
        except Exception as e:
          print(JsonResponse("Bad Request",safe=False))
