# How We Made The Thing

## Technologies

The main programming language of our project is Python. The website is implemented using Flask and Dash, and we keep long-term data in two sqlite databases - one for user accounts and one for financial data.

We developed an in-house library for analysing financial data, which covers the major metrics you would care about when backtesting. You can expect to see this extended further to support more advanced metrics for power-users.

Our financial database is kept up-to-date with a module known as the Data Harvester. It regularly collects and validates stock prices from a wide range of sources and sends them to our system.

## Process

Our software was developed using the Agile process. With weekly sprints, we were able to efficiently assign and complete tasks. [Something about adapting around unexpected difficulties here.]

Our code is hosted on a private repositary on GitHub, with the exception of the Data Harvester, which contains security-sensitive information. We use continuous integration to ensure that tests are run on every push, so that branches are not merged until all the tests are passing.

[Currently, this is about 1:10. Goal is 2:30.]