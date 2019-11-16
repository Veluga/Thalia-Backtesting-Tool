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



""" The models are the itnerface to the database, if you want to change attributes 
add or remove databases and keys, do it here also run makemigrations, and migrate.  """

class Portfolio(models.Model):
    portfolioID = models.IntegerField(default=1)
    Created = models.DateTimeField(auto_now_add=True, blank=True)

    """ Defines how to show the isntances as strings """
    def __str__(self):
        return (str(self.portfolioID) + ", Created: " + str(self.Created))



class Asset_temp(models.Model):
    # The first element in each tuple is the actual value to be set on the model, 
    # and the second element is the human-readable name. 
    ASSETCLASSES = [
        ("COMMODITIES", 'Commodities'), 
        ("CRYPTO", 'Cryptocurrency'),
        ("EQUITIES", 'Equities'),
        ("FOREX", 'FOREX'),
        ("FIXED", 'Fixed Income'),
    ]

    portfolioID = models.ForeignKey(Portfolio,on_delete=models.CASCADE)
    assetclass = models.CharField(max_length=100,choices=ASSETCLASSES,)
    # So you could like choose the assetclass then choose a category in it...
    # Need JS, so for now...
    category = models.CharField(max_length=100,choices=assetclasses.COMMODITIES,)
    percentage = models.IntegerField()

    """ Defines how to show the isntances as strings """
    def __str__(self):
        return (self.category + ": " + str(self.percentage))
