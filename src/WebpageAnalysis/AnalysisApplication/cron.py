from .models import WebPage
from datetime import datetime

def clear_outdated_entries():
    print("hello")
    WebPage.objects.filter(delete_on__lte = datetime.now()).delete()
