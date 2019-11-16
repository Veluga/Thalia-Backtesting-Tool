'''
 class responsible for generating key strategy figures
                   of a portfolio

'''

from datetime import date
from decimal import Decimal
from userPortfolio import Portfolio
import numpy as np


class keyFigureGenerator:

    @property
    def bestYear(self):
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
        return max([value for key, value in yrItems])

    @property
    def worstYear(self):
        '''
        the worst overall return IN A YEAR
        - if timespan within 1 year return THAT
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
        return min([value for key, value in yrItems])

    @property
    def maxDrawdown(self):
        '''
        calculate the max drawdown of portfolio between start and end date
        expressed in percentages
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
        return mdd

    @property
    def ROI(self):
        # firt calculate portfolio ROI and store it
        return (self.values[-1][1] - self.values[0][1]) / self.values[0][1]

    @property
    def CAGR(self):
        '''
        calculate the compound annual growth rate for the portfolio
        '''
        # get number of years
        # do parts of years since formula allows for it
        # TODO: Care about gap years? This miht in some sence be more accurate
        nYears = Decimal(len(self.values) / Decimal('365.25'))
        quotient = (self.values[-1][1] / self.values[0][1])
        return (quotient ** nYears) - Decimal(1)

    @property
    def sharpe(self):
        '''
        calculate portfolio ROI, risk free rate and sharp ratio
        '''
        # WARNING: Ignoring inflation
        # Modern inflation rates dont affect the sharp ration; Citation:
        # https://towardsdatascience.com/
        # calculating-sharpe-ratio-with-python-755dcb346805
        vals = [val[1] for val in self.values]
        return Decimal(np.std(vals) / Decimal(np.mean(vals)))

    @property
    def sortino(self):
        '''
        calculate sortino ratio
        '''
        # get all negative returns
        negReturns = []

        for i in range(len(self.values) - 1):
            if((self.values[i][1] - self.values[i+1][1]) < 0):
                negReturns.append(abs(self.values[i][1] - self.values[i+1][1]))

        if(len(negReturns) == 0):
            return None
        stdRets = np.std(negReturns)
        # compute std dev of negative returns
        if(stdRets == Decimal('0')):
            return None

        #get mean of daily returns
        mean = np.mean([val[1] for val in self.values])
        print(mean)
        print(str(stdRets)+ 'HelloWorlds')
        return Decimal(mean) / Decimal(stdRets)

    @property
    def initialBalance(self):
        '''
        simple getter for initial balance
        '''
        return self.initialBal

    @property
    def finalBalance(self):
        '''
        initialBalance: Decimal representing the initial
            balance of the portfolio
        '''
        # get final balance percentage
        # return final balance value
        return (self.initialBal) * (self.values[-1][1] / 100)

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
        self.initialBal = initialBalance
        self.values = self.portfolio.values(self.startDate, self.endDate)


'''
Testing code; dont mess with this; dont use this; remove this;
'''
if __name__ == '__main__':
    porto = Portfolio({'ass1': 0, 'ass2': 1, 'ass3': 0, 'ass4': 0, 'ass5': 0})
    kfg = keyFigureGenerator(porto,
                             date(day=1, month=10, year=2019),
                             date(day=29, month=10, year=2030),
                             Decimal('200'))
    print(kfg.initialBalance)
    print(kfg.finalBalance)
    print(kfg.worstYear)
    print(kfg.bestYear)
    print(kfg.maxDrawdown)
    print(kfg.sharpe)
    print(str(kfg.sortino))
