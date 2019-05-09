from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class CustomException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Custom Exception Message"
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


def raise_generic_url_exception():
    raise CustomException(detail={"Problem": "There was a problem trying to reach the provided url. \
    Make sure it is valid and reachable. Make sure it contains an http declaration such as 'https://' at the beginning"},
    status_code=status.HTTP_400_BAD_REQUEST)

def raise_specific_urllib_exception(error):
    from urllib.error import HTTPError
    raise CustomException(detail={"Problem": "There was a problem trying to reach the provided url. \
    Make sure it is valid and reachable. Make sure it contains an http declaration such as 'https://' at the beginning.\
    It is possible that the given page restricts our API from accessing it, in which case we can not work with it.",
    "Error": error}, status_code=error.code)

def raise_url_not_passed_exception():
    raise CustomException(detail={"Problem": "The request expected the query parameter url but did not receive it. \
    Correct your request by adding '?url=www.someurl.com' to the end of you request URI or adding the parameter 'url' to your request."},
    status_code=status.HTTP_417_EXPECTATION_FAILED)
