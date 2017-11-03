from corebase.test.institution_utils import create_institution, create_url
from institution.models import NotificationURL
from django.contrib.auth.models import User


def check_demo_institution():
    user = User.objects.filter(is_superuser=True).first()
    if not  NotificationURL.objects.filter(is_demo=True).exists():
        institution2 = create_institution(user)
        url = "http://localhost:8000/notify"
        create_url(institution2, url=url, is_demo=True)