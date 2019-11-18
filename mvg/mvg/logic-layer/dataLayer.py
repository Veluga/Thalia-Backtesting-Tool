'''
Mock up of data layer for testing
'''
import datetime
from decimal import Decimal


def getAssetPrices(asset, startDate, endDate):
    '''
    returns list of [date:price] for each day between startDate and endDate
    includes all data thats available
    WARNING: REMOVE THIS WHEN ACTUAL DATA LAYER IMPLEMENTED!!!
    ## TODO: MODIFY THIS SO STARTDATE AND ENDDATE HAVE MEANING
    ## TODO: ADD AN OPTION THAT ISNT FULLY DEFINED FOR TESTING INCOMPLETE DATA
    '''

    if(asset == 'ass1'):
        values = []
        currDate = datetime.date(month=10, day=1, year=2019)
        for a in range((endDate - startDate).days):
            values.append([currDate + datetime.timedelta(days=a), Decimal(5)])
        return values
    elif(asset == 'ass2'):
        values = []
        currDate = datetime.date(month=10, day=1, year=2019)
        for a in range((endDate - startDate).days):
            values.append([currDate + datetime.timedelta(days=a),
                          Decimal(a + 1)])
        return values
    elif(asset == 'ass3'):
        values = []
        currDate = datetime.date(month=10, day=1, year=2019)
        for a in range((endDate - startDate).days):
            values.append([currDate + datetime.timedelta(days=a),
                          Decimal((endDate - startDate).days - a + 1)])
        return values
    elif(asset == 'ass4'):
        # step function | step down
        values = []
        currDate = datetime.date(month=10, day=1, year=2019)
        for a in range((endDate - startDate).days):
            values.append([currDate + datetime.timedelta(days=a),
                          Decimal('10')])
        for a in range(int((endDate - startDate).days / 2)):
            values[a][1] = Decimal('5')
        return values
    elif(asset == 'ass5'):
        # step up
        values = []
        currDate = datetime.date(month=10, day=1, year=2019)
        for a in range((endDate - startDate).days):
            values.append([currDate + datetime.timedelta(days=a),
                          Decimal('1')])
        for a in range(int((endDate - startDate).days / 2)):
            values[a][1] = Decimal('5')
        return values
    return []


def getInflationRates(year, currency):
    '''
    Fake it till you make it~
    '''
    # lol
    return 2
