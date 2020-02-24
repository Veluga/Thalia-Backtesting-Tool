# 

| Use Case       | Backtest strategy                                                                                                                                                                                                                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Actors         | User                                                                                                                                                                                                                                                                                                                            |
| Purpose        | Show a user how their strategy would have performed in the past.                                                                                                                                                                                                                                                                |
| Overview       | The user selects they assets they want in their portfolio, along with how much to invest in each asset. They may select contribution/withdrawl and rebalancing options also. On completion, the user will see a graph plotting the value of their portfolio over time and a table of a few key metrics summarising performance. |
| Preconditions  | The user must be logged in.                                                                                                                                                                                                                                                                                                     |
| Postconditions | ?                                                                                                                                                                                                                                                                                                                               |

### Flow of Events

| Actor Action                                                                                                              | System Response                                                       |
| ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| 1. The user navigates to the **backtest** page of the website.                                                            |                                                                       |
| 2. The user selects a financial asset.                                                                                    |                                                                       |
| 3. The user enters the relative weight that asset                                                                         |                                                                       |
| 4. Steps 2 and 3 repeat any number of times                                                                               |                                                                       |
| 5. (Optional) The user selects how often to rebalance their portfolio. If nothing is selected, no rebalancing is assumed. |                                                                       |
| 6. (Optional) The user selects how often to contribute to/withdraw from their portfolio.                                  |                                                                       |
| 7. (Iff 6 occurred) The user enters the amount of money they contribute/withdraw at each contribution/withdrawl.          |                                                                       |
| 8. The user submits their strategy for evaluation                                                                         |                                                                       |
|                                                                                                                           | 9. The system analyses the user's strategy over the specified period. |
| 10. The user receives their strategy's performance.                                                                       |                                                                       |




