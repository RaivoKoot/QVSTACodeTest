from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
from bs4 import Doctype
import re

from ..exceptions import CustomException
from rest_framework import status

def analyze_page(url):

    try:
        # this line can cause 404 errors and possibly more if the url is
        # bad or something else with the page is wrong
        uClient = uReq(url)
    except HTTPError as error:
        raise CustomException(detail={"Problem": "There was a problem trying to reach the provided url. Make sure it is valid and reachable. Make sure it contains an http declaration such as 'https://' at the beginning", "Error": error}, status_code=error.code)
    except:
        raise CustomException(detail={"Problem": "There was a problem trying to reach the provided url. Make sure it is valid and reachable. Make sure it contains an http declaration such as 'https://' at the beginning"}, status_code=status.HTTP_400_BAD_REQUEST)


    # load html content
    page_html = uClient.read()
    uClient.close()

    html_version = find_html_version(page_html)

    # get html content as soup
    page_soup = soup(page_html, "html.parser")

    page_title = page_soup.title.string

    h1_count = len(page_soup.find_all('h1'))
    h2_count = len(page_soup.find_all('h2'))
    h3_count = len(page_soup.find_all('h3'))
    h4_count = len(page_soup.find_all('h4'))
    h5_count = len(page_soup.find_all('h5'))
    h6_count = len(page_soup.find_all('h6'))

    headings = [h1_count, h2_count, h3_count, h4_count, h5_count, h6_count]

    link_data = find_link_data(url, page_soup)

    analysis = {
        'html_version': html_version,
        'title': page_title,
        'headings': headings,
        'internal_links': link_data['internal_links'],
        'external_links': link_data['external_links'],
        'inaccessible_links': -1,
        'has_loginform': False,
    }

    return analysis

def find_link_data(url, page_soup):
    from urllib.parse import urlparse
    base_url = urlparse(url).netloc

    internal_links = 0
    external_links = 0
    inaccessible_links = 0

    # iterates over every link on the page
    for link in page_soup.find_all('a', href=True):
        link_base_url = urlparse(link['href']).netloc

        if link_base_url == '' or link_base_url == base_url:
            internal_links = internal_links + 1
        else:
            external_links = external_links + 1

    return {'internal_links': internal_links, 'external_links': external_links}




def find_html_version(page_html):
    # turns the html from byte-format into a string object
    page_html_string = page_html.lower().decode('utf-8')
    document_version = 'html version could not be found' # default

    HTML_5 = '<!doctype html>'
    # HTML 4.01 Strict
    HTML_4_STRICT = '<!doctype html public "-//w3c//dtd html 4.01//en"'
    # HTML 4.01 Transitional
    HTML_4_TRANSITIONAL = '<!doctype html public "-//w3c//dtd html 4.01 transitional//en"'
    # HTML 4.01 Frameset
    HTML_4_FRAMESET = '<!doctype html public "-//w3c//dtd html 4.01 frameset//en"'

    # tries to find an html version-tag in the page's html
    if HTML_5 in page_html_string:
        document_version = 'HTML 5'
    elif HTML_4_STRICT in page_html_string:
        document_version = 'HTML 4.01 Strict'
    elif HTML_4_TRANSITIONAL in page_html_string:
        document_version = 'HTML 4.01 Transitional'
    elif HTML_4_FRAMESET in page_html_string:
        document_version = 'HTML 4.01 Frameset'

    return document_version
