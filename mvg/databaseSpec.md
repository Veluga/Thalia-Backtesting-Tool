# INFORMATION PERTAINING TO THE DATA SEEDED IN THALIA DEMO DATABASE

Specification of dates withing witch price data for each seeded index is defined. Attempts to query outside of these ranges
will break demo software!


*Query to use for checking*

'''SQL

SELECT *
FROM portfolio_value, portfolio_asset
WHERE portfolio_value.asset_id = portfolio_asset.id AND portfolio_asset.abbreviation = 'DOW'
ORDER BY ASC/DESC


'''

|Index | Data available up to | Data available from|
|------|---------------------|------------------|
| Dow Jones | 2019-10-07 | 1985-01-29 |
| NASDAQ | 2019-10-07 | 1971-02-08 |
| S&P500 |2019-10-07 | 1927-12-30 |



