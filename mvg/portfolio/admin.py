from django.contrib import admin
from .models import Asset,Portfolio
# Register your models here.
# This is to view the db in admin, which is a nice interface to it.

admin.site.register(Asset)
admin.site.register(Portfolio)