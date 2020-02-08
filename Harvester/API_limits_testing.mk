#API limits
Internal Use Only 
##nomics
We have 10 cryptos,the main ones and all the curencies I could found.
That is 125 in total even if we would add more cryptos 200 calls per day should be enough. Keep in mind that all the results are USD and it might require some conversions. In that Case more than 200 could be required.


####Documentation Sources
They say it is free to use and there are no limits

Test:	

	200 API calls 2 months worth of data
	result: Passed 
	time: under 3 minutes
	
	
	Another 1000 API calls all data on BTC each transfer
	remarks: they emailed to tell me that they are happy that I use their product
	result: It slows you done after 300 calls but it still works
	time: 6 minutes for ~200 , 2 minutes per 100 calls after that
		might depend on the time of day


##yfinance
####Documentation sources
Found 2 websites related to their product with 2 different results.
RapidAPI has: 500 calls/month (how do they know it is you ???)
There is some relation between YQL and yfinance API both should have the same characteristics some say : 2.000/hour per IP

####Empirical tests not conducted by me
Up to 6000 requests daily followed by a 999 HTTP code that should be seen as too many requests
####Tests done by me
WIth API key :
yfinance does not do that anymore 

Without API key :
tested trough a VPN in case of IP block
First test:

	Count time for 100 api calls, 1 day. 
		result: 2 minutes 45 seconds
	Cont time for 100 api calls 30 years 
		result: 3 minutes 10 seconds

Second Test:
	
	1200 api calls 1 day retrieval
		Remarks: it starts to became slower after the first 300 	
	result: passed in <10 minutes
	7200 api calls in day 
	result: after 5702 the VPN disconnected me
This seems to be a good number of calls until now
: 

Restarted and waiting for the API to block me
result:	

	Laptop battery run out
