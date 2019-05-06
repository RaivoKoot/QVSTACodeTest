from django.db.models.query import QuerySet
from datetime import datetime

class WebPageQuerySet(QuerySet):

    def webscrape_or_get(self, url):
        from ..models import WebPage

        resultSet = self.filter(url=url).order_by('-pk')[:1]
        analysis = resultSet.first()

        # The given url has no cached data
        if(analysis == None):
            # perform new webscraping
            print()

        # The given url has cached data. However it is outdated and has
        # not been automatically deleted yet by the regular jobs.
        # The replace() method is used to avoid problems caused by timezones
        elif(datetime.now() > analysis.delete_on.replace(tzinfo=None)):
            # Therefore, delete it and perform new webscraping
            analysis.delete()
            # perform new webscraping


        return resultSet
