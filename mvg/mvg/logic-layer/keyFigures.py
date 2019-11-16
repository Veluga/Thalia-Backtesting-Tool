'''
 class responsible for generating key strategy figures
                   of a portfolio


Arthur-Louis Heath
1.11.2019
'''


from datetime import date
from decimal import Decimal
from portfolio import Portfolio
import numpy as np


class keyFigureGenerator:
    def __calcBestWorstYears__(self):
        '''
        return the year with the worst overall return
        - if timespan within 1 year return that one
        '''
        # check if timespan within one year
        if(self.startDate.year == self.endDate.year):
            return self.startDate.year

        allVals = self.values
        yearlyReturns = {}
        # group by years
        yearStart = self.startDate
        for yearNo in range(self.endDate.year - self.startDate.year + 1):
            year = self.startDate.year + yearNo
            # get days from start till end of year
            numDays = (min(date(day=1,
                                month=1,
                                year=(year + 1)),
                           allVals[-1][0]) - yearStart).days
            # add to dict if full year
            # TODO: what if we finish one day before the end of a gap year?
            yearStart = date(day=1, month=1, year=(year + 1))
            if(not(numDays == 365 or numDays == 366)):
                continue
            # seperate from array
            currYear = allVals[:numDays]
            allVals = allVals[numDays:]
            # calculate overall return for year
            # WARNING: try setting to 0; theres a Decimal() missing somewhare
            overallReturn = (currYear[-1][1] - currYear[0][1]) / currYear[0][1]
            yearlyReturns[year] = overallReturn

        yrItems = yearlyReturns.items()
        self.bestYear = max([(value, key) for key, value in yrItems])[1]
        self.worstYear = min([(value, key) for key, value in yrItems])[1]

    def __calcMaxDrawdown__(self):
        '''
        calculate the max drawdown of portfolio between start and end date
        expressed in percentages

        store it in self.mdd
        '''
        # things to track
        peak = self.values[0][1]
        trough = self.values[0][1]
        mdd = Decimal(0)
        for val in self.values:
            # if we found a new peak, reset mdd
            if(val[1] >= peak):
                peak = val[1]
                trough = val[1]
            # if we found a new low
            if val[1] < trough:
                trough = val[1]
                # is this a new max dd?
                if (peak - trough) > mdd:
                    mdd = (peak - trough)
        self.mdd = mdd

    def __calcROI__(self):
        # firt calculate portfolio ROI and store it
        self.roi = (self.values[-1][1] - self.values[0][1]) / self.values[0][1]

    def __calcCAGR__(self):
        '''
        calculate the compound annual growth rate for the portfolio

        save it in self.cagr
        '''
        # get number of years
        # do parts of years since formula allows for it
        # TODO: Care about gap years? This miht in some sence be more accurate
        nYears = Decimal(len(self.values) / Decimal('365.25'))
        mySanityIsFlaking = (self.values[-1][1] / self.values[0][1])
        self.cagr = (mySanityIsFlaking**nYears) - Decimal(1)

    def __calcRiskFreeSharp__(self):
        '''
        calculate portfolio ROI, risk free rate and sharp ratio

        save sharp ratio to self.sharp
        '''
        # WARNING: Ignoring inflation
        # Modern inflation rates dont affect the sharp ration; Citation:
        # https://towardsdatascience.com/
        # calculating-sharpe-ratio-with-python-755dcb346805
        flakeSucks1 = np.std([val[1] for val in self.values])
        flakeSucks2 = np.mean([val[1] for val in self.values])
        self.sharp = Decimal(flakeSucks2) / Decimal(flakeSucks1)

    def __calcSortino__(self):
        '''
        MAR: minimum acceptible roi
        calculate sortino ratio
        '''
        # get all negative returns
        negReturns = []
        for i in range(len(self.values) - 1):
            if((self.values[i][1] - self.values[i+1][1]) < 0):
                negReturns.append(abs(self.values[i][1] - self.values[i+1][1]))

        print(negReturns)
        stdRets = np.std(negReturns)
        print(str(stdRets) + ' SDTD RETS')
        # compute std dev of negative returns
        if(stdRets < Decimal('0.00001')):
            self.sortino = None
            return
        lintingWasAMistake = np.mean([val[1] for val in self.values])
        self.sortino = Decimal(lintingWasAMistake) / Decimal(stdRets)

    def getSortino(self):
        '''
        getter for sortino
        '''
        return self.sortino

    def getCAGR(self):
        '''
        getter for compound annual growth rate
        '''
        return self.cagr

    def getMaxDrawdown(self):
        '''
        getter for max drawdown
        '''
        return self.mdd

    def getROI(self):
        '''
        getter for portfolio ROI
        '''
        return self.roi

    def getBestYear(self):
        '''
        simple getter for best Year
        '''
        return self.bestYear

    def getWorstYear(self):
        '''
        simple getter for worst year
        '''
        return self.worstYear

    def getInitialBalance(self):
        '''
        simple getter for initial balance
        '''
        return self.initialBalance

    def getFinalBalance(self):
        '''
        initialBalance: Decimal representing the initial
            balance of the portfolio
        '''
        # get final balance percentage
        # return final balance value
        return (self.initialBalance) * (self.values[-1][1] / 100)

    def getSharp(self):
        # getter for portfolio Sharp Ratio
        return self.sharp

    # constructor
    def __init__(self, portofolio, startDate, endDate, initialBalance):
        '''
        portofolio: portfolio object as deined in portfolio.py
        startDate: datetime.date date from witch to start calculation
        endDate: datetime.date date at witch to end calculation
        '''
        self.portfolio = portofolio

        self.startDate = startDate

        self.endDate = endDate

        self.initialBalance = initialBalance

        self.values = self.portfolio.getValues(self.startDate, self.endDate)

        self.__calcBestWorstYears__()
        self.__calcMaxDrawdown__()
        self.__calcCAGR__()
        self.__calcROI__()
        self.__calcRiskFreeSharp__()
        self.__calcSortino__()


'''
Testing code; dont mess with this; dont use this; remove this;
'''
if __name__ == '__main__':
    porto = Portfolio({'ass1': 0, 'ass2': 0, 'ass3': 0, 'ass4': 1, 'ass5': 0})
    kfg = keyFigureGenerator(porto,
                             date(day=1, month=10, year=2019),
                             date(day=29, month=10, year=2030),
                             Decimal('200'))
    print(kfg.getInitialBalance())
    print(kfg.getFinalBalance())
    print(kfg.getWorstYear())
    print(kfg.getBestYear())
    print(kfg.getMaxDrawdown())
    print(kfg.getSharp())
    print(str(kfg.getSortino()) + '<----Sortino')
