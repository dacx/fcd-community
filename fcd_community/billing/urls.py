from django.urls import path

from fcd_community.billing.views import billing_home

app_name = "billing"

urlpatterns = [
    path("", view=billing_home, name="home"),
]
