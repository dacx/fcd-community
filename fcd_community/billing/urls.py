from django.urls import path

from fcd_community.billing.views import billing_home, checkout_session, checkout_success

app_name = "billing"

urlpatterns = [
    path("", view=billing_home, name="home"),
    path("checkout", view=checkout_session, name="checkout"),
    path("checkout/success", view=checkout_success, name="checkout_success"),
]
