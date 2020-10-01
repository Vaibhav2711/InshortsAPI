from rest_framework import serializers
from snippets.models import Snippet
from snippets.inshorts import getNews
class Serializer(serializers.ModelSerializer): 
  class Meta:
        model = Snippet
        fields = ['id','category','val']
