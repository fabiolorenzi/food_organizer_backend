"""
URL configuration for food_organizer_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import users, week_plans, expenses, products

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("api/v1/users", users.users_list),
    path("api/v1/users/<int:id>", users.user_single),
    path("api/v1/users/login", users.user_login),
    path("api/v1/users/user", users.user_single_user),
    path("api/v1/week-plans", week_plans.week_plan_list),
    path("api/v1/week-plans/<int:id>", week_plans.week_plan_single),
    path("api/v1/expenses", expenses.expense_list),
    path("api/v1/expenses/<int:id>", expenses.expense_single),
    path("api/v1/products", products.product_list),
    path("api/v1/products/<int:id>", products.product_single)
]
