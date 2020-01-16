# Requirements

We classify our requirements using the established FURPS+ model. Below you will see our main functional and non-functional requirements. The items outlined below focus on some of the key requirements we have so far identified as features necessary to provide a compelling product for paying customers.

## Functional requirements

| **Create portfolio**                                              |                                                                                                                       |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Specify fixed amount/proportions of the portfolio to given assets | Choose how much each asset contributes to the portfolio's total value using either percentages or raw monetary amounts |
| Find assets quickly by category or name                           | When adding an asset the user can search a category for assets or search for a specific asset by its name             |
| Share portfolio                                                   | Portfolio's can be shared between people using a URL                                                                   |
| Edit portfolio                                                   |  Change included assets and their distributions in a portfolio                                                          |

| **Setup portfolio analysis**                                      |                                                                                                                                      |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Compare portfolios                                         | Use multiple portfolios in a single analysis to see differences in their performance                                                        |
| Compare portfolios performance against standard strategies | Select predefined strategies to compare your (e.g. S&P 500) strategy against, such                                                                       |
| Use given lazy portfolios                                  | Select an existing common portfolio to compare against such as common index funds (e.g. Vanguard 500 Index Investor or SPY).                                                  |
| Plot portfolio as a time-series                            | View portfolio performance as a line graph for quick overview                                                                        |
| Specify a time frame for the analysis                       | Select start and end dates for portfolio analysis                                                                                           |
| Choose re-balancing strategy                               | Optionally choose a strategy for buying and selling assets to meet your strategy e.g. buying and selling stocks each year to ensure the value of portfolio stays at 60% stocks and 40% bonds |
| Changes the distribution of assets in a portfolio using a slider  | A slider for each asset to quickly increase or decrease it's proportion of the total value |
| Edit portfolio analysis | Change parameters for portfolio's analysis after running it (e.g. date range or re-balancing strategy) |

| **View results**                                       |                                                                                                                                                               |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| See key numerical figures                                 | Shows important numerical metrics for a portfolio's performance such as Initial balance, Standard deviation, Worst year, Sharpe Ratio, Sortino Ratio |
| See both real and nominal values                          | See portfolio's value as both adjusted and not adjusted for inflation                                                                                          |
| A breakdown of portfolio value at specific points of time | See what the value of the portfolio is at each specified time period such as each year or month                                                               |
| Export analysis results                                   | Exports results to PDF for sharing and offline reading                                                                                                                         |

| **User accounts**           |                                                           |
| --------------------------- | --------------------------------------------------------- |
| Combine portfolios          | Combine two portfolios' assets into one single portfolio          |
| Save portfolio analysis for later    | Save portfolio analysis parameters to the account so you can rerun it with a single click  |
| Delete saved portfolio analysis      | Remove a stored portfolio analysis from your account |
| Manage portfolio analyses          | Edit saved portfolio analysis with different assets, distributions or other parameters     |
| Sign-up, log in and log out | Basic authentication                                      |

| **Assets**                                                                               |                                                                                               |
| ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Choose assets from European market                                                       | Having data for European assets was found to be lacking in competing products |
| Choose assets from Equities, Fixed Income, Currencies, Commodities, and Cryptocurrencies | TBD |

## Non-functional requirements

- Usability

  - The product must be easily usable for users who already have some financial investment experience.

  - Basic backtesting interface needs to look familiar to people already experienced with backtesting.

  - The product will have detailed instructions on how to use its advertised functions.

  - All major functions must be visible from the initial landing page.

  - Must work in both desktop and mobile browsers.

  - The results page should scale with mobile.

- Reliability

  - The product must have a greater than 99% uptime.

  - All our assets need to have up to date daily data where the asset is still publicly tradeable.

  - All assets supported by the system must provide all publicly available historical data.

- Performance

  - The website should load within 3 seconds on mobile [Google Data, Global, n=3,700 aggregated, anonymized Google Analytics data from a sample of mWeb sites opted into sharing benchmark data, March 2016.].

  - Large portfolios must be supported - up to 300 different assets.

- Implementations

  - The system needs to work on a cloud hosting provider.

- Interfacing

  - The data gathering module must never use APIs stated to-be-deprecated within a month.

  - The data gathering module must not exceed it's contractual usage limits.

- Operations

  - An administrator on call will be necessary for unexpected issues.

- Packaging

  - The product needs to work inside a Linux container (e.g. Docker).

- All dependencies need to be installable with a single command.

- Legal

  - All user testing must be done with ethical approval from the University.

  - UI must display a clear legal disclaimer about the service not providing financial advice.

  - All third-party code should allow for commercial use without requiring source disclosure (e.g. no GPL-3).

  - User data handling should comply with GDPR.
