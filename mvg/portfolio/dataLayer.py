'''
Mock up of data layer for testing
'''
from datetime import datetime
from decimal import Decimal

from . import models

def getAssetPrices(assetName: str, startDate: datetime, endDate: datetime) -> [[datetime, Decimal]]:
    '''
    @param assetName: the ticker/abbreviation of the asset you want.
    startDate and endDate inclusive.
    '''
    
    assetVals = generateAssetsQuery(assetName)
    
    return sorted([
        [v.date, v.open_price] for v in assetVals
        if startDate <= datetime.combine(v.date, datetime.min.time()) <= endDate
    ])

def getAvailableAssets():
    pass


def generateAssetsQuery(abbr: str):
    '''
    Query all stored value of an asset, defined by 
    param: abbreviation
    '''
    return models.Value.objects.raw(
        'SELECT portfolio_value.id, portfolio_value.date, portfolio_value.open_price ' +
        'FROM portfolio_value, portfolio_asset ' +
        'WHERE portfolio_value.asset_id = portfolio_asset.id AND ' +
        f'portfolio_asset.abbreviation = \'{abbr}\''
    )

