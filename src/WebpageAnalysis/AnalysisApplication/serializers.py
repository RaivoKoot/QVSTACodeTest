from .models import WebPage, Heading
from rest_framework import serializers

class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = (
            'type',
            'count'
        )

class WebPageSerializer(serializers.ModelSerializer):
    headings = HeadingSerializer(source='headings_set', many=True)

    class Meta:
        model = WebPage
        fields = (
            'url',
            'html_version',
            'page_title',
            'internal_links',
            'external_links',
            'inaccessible_links',
            'has_loginform',
            'headings'
        )
