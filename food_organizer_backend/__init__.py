import django

django.setup()
from .models import user, week_plan, expense, product
from .views import users, week_plans, expenses, products
