from django.shortcuts import render
from AnalysisApplication.models import WebPage, Heading
from AnalysisApplication.serializers import WebPageSerializer, HeadingSerializer
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from AnalysisApplication.exceptions import *
from rest_framework import status

# Create your views here.

class WebPageList(generics.ListAPIView):
    serializer_class = WebPageSerializer

    def get_queryset(self):
        queryset = WebPage.objects.all()
        url = self.request.query_params.get('url', None)

        if url is not None:
            # reverse ordering so that the newest is the first
            # and then only take the first object
            queryset = queryset.webscrape_or_get(url)
        else:
            raise_url_not_passed_exception()

        return queryset
