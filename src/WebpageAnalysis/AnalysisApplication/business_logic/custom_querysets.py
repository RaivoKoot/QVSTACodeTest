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
            self.webscrape_and_save(url)
            resultSet = WebPage.objects.filter(url=url).order_by('-pk')[:1]

        # The given url has cached data. However it is outdated and has
        # not been automatically deleted yet by the regular jobs.
        # The replace() method is used to avoid problems caused by timezones
        elif(datetime.now() > analysis.delete_on.replace(tzinfo=None)):
            # Therefore, delete it and perform new webscraping
            analysis.delete()
            # perform new webscraping
            self.webscrape_and_save(url)
            resultSet = WebPage.filter(url=url).order_by('-pk')[:1]


        return resultSet

    def webscrape_and_save(self, url):
        from ..models import WebPage, Heading
        from .webscraping import analyze_page

        analysis_data = analyze_page(url)

        analysis = WebPage()
        analysis.url = url
        analysis.html_version = analysis_data['html_version']
        analysis.page_title = analysis_data['title']

        analysis.internal_links = analysis_data['internal_links']
        analysis.external_links = analysis_data['external_links']
        analysis.inaccessible_links = analysis_data['inaccessible_links']
        analysis.has_loginform = analysis_data['has_loginform']
        analysis.save()

        HEADING_TAGS = ['H1', 'H2', 'H3', 'H4','H5','H6']

        for heading_count, tag in zip(analysis_data['headings'], HEADING_TAGS):
            heading = Heading()
            heading.type = tag
            heading.count = heading_count
            heading.webpage = analysis
            heading.save()
