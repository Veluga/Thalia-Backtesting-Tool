'''

Class holding information and methods in regards to a single user portfolio

'''
from decimal import Decimal
from datetime import date, timedelta

import numpy as np
from operator import add

from . import dataLayer

class Portfolio:
    def values(self, startDate, endDate):
        '''
        Return series of values of portfolio on days between startDate and
        endDates expressed as percentages of the starting value
        - Method assumes data is continuous

        startDate: datetime.date to start from
        endDate: datetime.date to end at

        TODO: ADD SAFETY MEASURE IN CASE DATA NOT DEFINED; POLITELY
        SUGJEST CHECKING AND PRUNING
        ADD CHECK FOR LENGTH OF TIME INTERVAL ASWELL ITS USED LOWER DOWN!
        '''

        totals = [Decimal('0')] * (endDate - startDate).days
        for assetName in self.assets.keys():
            # WARNING: INTERFACING WITH VITUAL DATA LAYER!!!
            vals = dataLayer.getAssetPrices(assetName, startDate, endDate)

            # adjust prices to be expressed in percentages of starting price
            # also adjust for weights
            initialPrice = vals[0][1]
            vals = list(map(lambda x:
                            (x[1] / initialPrice) *
                            Decimal(100) *
                            self.assets[assetName], vals))
            totals = list(map(sum, zip(totals, vals)))

        # normalize
        totals = list(map(lambda x: (x / totals[0]) * Decimal(100), totals))
        # add dates back
        return [[startDate + timedelta(days=a),
                 totals[a]] for a in range(len(totals))]

    def assetCorrelations(self, startDate, endDate):
        '''
        Get correlation coefficient of each asset in regards to toal value of
        portfolio

        returns dict of form {asset id's:correlation coefficients}
        '''
        # calculate mean of portfolio values
        pfValues = [val[1] for val in self.values(startDate, endDate)]
        pfValMean = np.mean(pfValues)
        # calulate mean of all values for each asset
        keys = list(self.assets.keys())
        keys.sort()
        assetValues = []
        assetValMeans = []
        assetValStds = []
        for asset in keys:
            # WARNING: INTERFACING WITH VIRTUAL DATA LAYER
            av = [a[1] for a in dataLayer.getAssetPrices(asset,
                                                         startDate,
                                                         endDate)]
            assetValues.append(av)
            assetValMeans.append(np.mean(av))
            assetValStds.append(np.std(av))

        # calculate std dev of portfolio values
        pfValuesStdDev = np.std(pfValues)

        # calculate standardised values for portfolio values
        standardizedPfVals = [((val - pfValMean) / pfValuesStdDev)
                              for val in pfValues]
        # calculate standardised values for portfolio
        standardizedAssetVals = []
        for i in range(len(keys)):
            assetValStd = assetValStds[i]
            # stop zero devision error
            if assetValStds[i] == 0:
                standardizedAssetVals.append([0] * len(keys))
                continue
            standardizedAssetVals.append([((val - assetValMeans[i]) /
                                          assetValStd)
                                          for val in assetValues[i]])

        # Multiply standardised value list pairs
        pairs = (lambda x: list(map(add, x, standardizedPfVals)))
        standardizedAssetVals = list(map(pairs, standardizedAssetVals))

        # multiply list elements
        standardizedAssetVals = list(map(np.prod, standardizedAssetVals))
        # normalize values
        standardizedAssetVals = list(map(lambda x: x /
                                     (Decimal(len(pfValues)) +
                                      Decimal('1')), standardizedAssetVals))
        # put it in a cozy dictionary
        results = dict(zip(keys, standardizedAssetVals))
        return results

    def __init__(self,
                 assets):
        '''
        If not provided with an initial balance and currency portfolio
        operations will be expressed in percentage of original value

        assets: dictionary mapping asset identifiers to relative weights of
        each asset in portoflio
        '''
        # set assets dicitonary
        self.assets = assets

'''
if __name__ == '__main__':
    # porto = Portfolio({ 'ass1':1,'ass2':1, 'ass3':50,'ass4':50,'ass5':1})
    porto = Portfolio({'ass4': 50})
    # print(porto.getValues(12,12))
    print(porto.values(
                        date(day=1, month=10, year=2019),
                        date(day=5, month=10, year=2019)))
    print(porto.assetCorrelations(
                        date(day=1, month=10, year=2019),
                        date(day=29, month=10, year=2019)))
'''
