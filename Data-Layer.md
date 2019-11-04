# INTERFACES FOR DATA/BUSINESS LOGIC LAYER
Arhtur-Louis Heath; 4.11.2019

The following are the interface with the interface and data layers respectively,
as the data layer does not yet exist, I have implemented a vitual data layer that
my code interfaces with. This needs to be modified at a future date. Methods that
would merely pass data up to the interface layer from the data layer have also been
ommited. All data is assumed to be present, if we will be working with incomplete
data for our MVG changes will need to be made.

## Interface with user interface layer

### In portoflio.py:

  - *Portfolio(assets)*

Creates a portfolio object, accepts an argument that is a python dictionary where
each key represents an assetID (ticker) and maps to the relatie weight of the asset
in the portfolio. The weights do not need to total 100.
  - *Portfolio.getValues(startDate, endDate)*

Gets the total values of portfolio between two datetime date's. The values are expressed
in percentages of the starting values of the portfolio (at start date)
  - *Portfolio.getAssetCorrelations(startDate, endDate)*

Returns a dictionary that maps asset names in the portfolio to their correlation
to the overall portfolio price

### In keyFigures.py

  - *keyFigureGenerator(portofolio, startDate, endDate, initialBalance)*

Generates and holds the key figures for a portfolio between startDate and
end Date. initialBalance is the user defined balance at start of simulation and
defaults to 100 (represending everything in percentages)

  - *getSortino()*

Returns sortino ratio for portfolio. If there is not enough data, it will return None.

  - *getCAGR()*

Returns calculated anual growth rate for portfolio caluclated from daily returns.

  - *getMaxDrawdown()*

Returns the max drawdown of portfolio calculated from daily returns.

  - *getROI()*

Returns overall return on investment of portfolio between determined dates.

  - *getBestYear()*

Returns the Year with the highest return on investment. If all dates within a year,
it returns that year. If data only present for part of first/last year of simulation it
ignores those years.

  - *getWorstYear()*

Same a getBestYear

  - *getInitialBalance()*

Returns initial balance of portfolio as specified when creating object.

  - *getFinalBalance()*

Returns final balance of portfolio.

  - *getSharp()*

Returns simplified sharp ratio of portfolio. Ignores inflation as modern inflation rates are relatively
low. Source: **https://towardsdatascience.com/calculating-sharpe-ratio-with-python-755dcb346805**


## Interface with data layer

Needs to be able to retrieve list of continuous sequence of [datetime.date, decimal.Decimal] pairs representing values of an asset. Provides a startDate, endDate and assetID (ticker).