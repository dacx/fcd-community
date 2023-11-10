from django.urls import path

from fcd_community.plowing.views import plowing_home, plowing_service, manage_request

app_name = "plowing"

urlpatterns = [
    path("", view=plowing_home, name="home"),
    path("<str:service_id>/", view=plowing_service, name="service"),
    path("manage/<str:request_id>/", view=manage_request, name="request"),
]
