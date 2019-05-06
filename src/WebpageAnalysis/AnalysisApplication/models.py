from django.db import models
from datetime import datetime, timedelta

# Create your models here.
class WebPage(models.Model):
    url = models.URLField()
    html_version = models.CharField(max_length=20)
    page_title = models.CharField(max_length=100)
    internal_links = models.IntegerField()
    external_links = models.IntegerField()
    inaccessible_links = models.IntegerField()
    has_loginform = models.BooleanField()

    # the date on which this database row needs to be deleted:
    # 24 hours after creation
    delete_on = models.DateTimeField(default=datetime.now()+timedelta(days=1))

class Heading(models.Model):
    HEADING_TYPE_CHOICES = (
        ('H1', 'Heading Type 1'),
        ('H2', 'Heading Type 2'),
        ('H3', 'Heading Type 3'),
        ('H4', 'Heading Type 4'),
        ('H5', 'Heading Type 5'),
        ('H6', 'Heading Type 6')
    )

    type = models.CharField(
        max_length=2,
        choices=HEADING_TYPE_CHOICES
    )
    count = models.IntegerField()
    webpage = models.ForeignKey(
        WebPage,
        related_name='headings_set',
        on_delete=models.CASCADE
    )
