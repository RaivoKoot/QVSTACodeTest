from .models import WebPage
from datetime import datetime

def clear_outdated_entries():
    WebPage.objects.filter(delete_on__lte = datetime.now()).delete()
