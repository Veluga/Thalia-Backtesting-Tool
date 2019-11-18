from django.db import models
from datetime import datetime

from . import assetclasses


class AssetClass(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=255, unique=True)

    asset_class = models.ForeignKey(AssetClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Value(models.Model):
    open_price = models.DecimalField(max_digits=50, decimal_places=20)
    close_price = models.DecimalField(max_digits=50, decimal_places=20)
    high_price = models.DecimalField(max_digits=50, decimal_places=20)
    low_price = models.DecimalField(max_digits=50, decimal_places=20)

    date = models.DateField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.date}, {self.open_price}, {self.close_price}, "
                + f"{self.high_price}, {self.low_price}")


