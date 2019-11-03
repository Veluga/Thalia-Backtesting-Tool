from django.contrib import admin

from .models import AssetClass, Asset, Value

admin.site.register(AssetClass)
admin.site.register(Asset)
admin.site.register(Value)
