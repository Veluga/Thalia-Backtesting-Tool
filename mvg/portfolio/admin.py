from django.contrib import admin
from .models import Asset_temp,Portfolio
# Register your models here.
# This is to view the db in admin, which is a nice interface to it.

admin.site.register(Asset_temp)
admin.site.register(Portfolio)
