from django.shortcuts import render
from AnalysisApplication.models import WebPage, Heading
from AnalysisApplication.serializers import WebPageSerializer, HeadingSerializer
from rest_framework import generics

# Create your views here.

class WebPageList(generics.ListCreateAPIView):
    queryset = WebPage.objects.all()
    serializer_class = WebPageSerializer
