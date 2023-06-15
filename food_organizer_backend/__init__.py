import django

django.setup()
from .models import user, week_plan
from .views import users
