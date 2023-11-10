from django.contrib import admin

from fcd_community.plowing.models import PlowingService, PlowingRequest

# Register your models here.
admin.site.register(PlowingService)
admin.site.register(PlowingRequest)
