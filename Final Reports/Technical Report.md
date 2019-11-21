# Requirements

We classify our requirements using the established FURPS+ model [citation needed]. Below you will see our main functional and non-functional requirements. The items outlined below focus on some of the key requirements we have so far identified as features necessary to provide a compelling product for paying customers.

## Functional requirements

| **Portfolio Configuration**                                        |                                                                                                                         |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Allocate fixed amount/proportions of the portfolio to given assets | Choose how much each asset contributes to the portfolio's total value using either percentages or raw monetary amounts. |
| Find assets quickly by category or name                            | When adding an asset the user can search a category for assets or search for a specific asset by its name               |
| Share portfolio                                                    | Portfolios can be shared between people using a URL                                                                     |
| Edit portfolio                                                     | Change asset allocation and their distributions in a portfolio                                                          |

| **Setup portfolio analysis**                                     |                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------- |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Compare portfolios                                               | Use multiple portfolios in a single analysis to see differences in their performance                                                                                                                                                |
| Compare portfolio's performance against standard strategies      | Select predefined strategies to compare your (e.g. S&P 500) strategy against                                                                                                                                                        |
| Use a selection of  lazy portfolios                              | Select an existing common portfolio to compare against such as common index funds (e.g. Vanguard 500 Index Investor or SPY)                                                                                                         |
| Plot portfolio as a timeseries                                   | View portfolio performance as a line graph for quick overview                                                                                                                                                                       |
| Specify a time frame for the analysis                            | Select start and end dates for portfolio analysis                                                                                                                                                                                   |
| Choose rebalancing strategy                                      | Optionally choose a strategy for buying and selling assets to meet your strategy e.g. buying and selling stocks each year to ensure the value of portfolio stays at 60% stocks and 40% bonds (i.e. maintain the initial allocation) |
| Changes the distribution of assets in a portfolio using a slider | A slider for each asset to quickly increase or decrease its proportion of the total value                                                                                                                                           |
| Edit portfolio analysis                                          | Change parameters for portfolio's analysis after running it (e.g. date range or rebalancing strategy)                                                                                                                               |

| **View results**                                          |                                                                                                                                                      |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| See key numerical figures                                 | Shows important numerical metrics for a portfolio's performance such as Initial balance, Standard Deviation, Worst Year, Sharpe Ratio, Sortino Ratio |
| See both real and nominal values                          | See portfolio's value as both adjusted and not adjusted for inflation                                                                                |
| A breakdown of portfolio value at specific points of time | See what the value of the portfolio is at each specified time period such as each year or month                                                      |
| Export analysis results                                   | Exports results to PDF for sharing and offline reading                                                                                               |

| **User accounts**                 |                                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------------- |
| Combine portfolios                | Combine two portfolios' assets into one single portfolio                                  |
| Save portfolio analysis for later | Save portfolio analysis parameters to the account so you can rerun it with a single click |
| Delete saved portfolio analysis   | Remove a stored portfolio analysis from your account                                      |
| Manage portfolio analyses         | Edit saved portfolio analysis with different assets, distributions or other parameters    |
| Sign-up, log in and log out       | Basic authentication                                                                      |

| **Assets**                                                                               |                                                                               |
| ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Choose assets from European market                                                       | Having data for European assets was found to be lacking in competing products |
| Choose assets from Equities, Fixed Income, Currencies, Commodities, and Cryptocurrencies | Coverage of some of the largest asset classes                                 |

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
  
  - The website should load within 3 seconds on mobile [1].
  
  - Large portfolios must be supported - up to 300 different assets.

- Implementations
  
  - The system needs to work on a cloud hosting provider.

- Interfacing
  
  - The data gathering module must never use APIs stated to-be-deprecated within a month.
  
  - The data gathering module must not exceed its contractual usage limits.

- Operations
  
  - An administrator on-call will be necessary for unexpected issues.

- Packaging
  
  - The product needs to work inside a Linux container (e.g. Docker).

- All dependencies need to be installable with a single command.

- Legal
  
  - All user testing must be done with ethical approval from the University.
  
  - UI must display a clear legal disclaimer about the service not providing financial advice.
  
  - All third-party code should allow for commercial use without requiring source disclosure (e.g. no GPL-3).
  
  - User data handling should comply with GDPR.

# Architecture Choice

We started by looking at the main architecture types [2] and checking their advantages and disadvantages with respect to the specifics of our application. This has helped us greatly reduce the number of candidate architectures. The remaining ones specific to web developement were *Client-Server*, *Data Centric* and the *Layered* types. The options that proved to be the most advantageous were the *Hexagonal* and the *Three Layer* architectures. However, due to the fact that the key point of our application is data collection and processing, it was decided that steps should be taken in order to isolate the financial data management. As a result doing this we have modified our *Hexagonal* architecture to include a marginal *Financial Data Manager*. For the *Three Layer* architecture we have added a extra layer below the data storage layer. After comparing the two we have decided that the modified *Three Layer* had a more clear representation of our application.

# Architecture Diagram

![Simple Architecture Diagram](./Resources Technical Report/simple_architecture_diagram.png)

# Reasoning for making a Financial Data Retrieval layer

The first argument comes from the need of extra Security. Guidelines have been obtained from the National Cyber Security Centre for Separation and cloud security [3]. While the data we have can be found for free in small quantities, getting it from multiple sources and storing it all in one place make it have financial value. In addition this is a good way to make sure that we have a clear-cut control procedures over our data. By giving the web-server limited permissions to the to the financial data, we limit the type of attacks that can take place. In addition, by not including the financial data retrieval in the business logic core allows for added availability since the web-sever and the data retrieval can work independently and can be modified independently. In addition the calls to the financial application programming interfaces require private keys that we want to keep in a more secure manner than having the web server have access to them. An additional argument would clean data flow provided by this architecture.

# Layer View of the Architecture

![Layer View of the Architecture](./Resources Technical Report/module_diagram.png)

# Portfolio Data Representation

We have chosen to create two separate data types for a portfolio - one for its specification (how much to invest in what) and one for its performance (how much money one has at a given moment in time). The client constructs the specification based on user input and sends it to the server. Once received, the server does the necessary computations and sends back the portfolio performance to the client.

Benefits:

- The client does not need to have a high-end CPU to get their information quickly.

- Minimal information is passed over networks, which can be slow and unreliable.

Drawbacks:

- The response time might be increased when doing intensive numerical calculations for multiple clients.

# Data Harvester

It connects to a series of financial application programming interfaces and continuously updates the data based on the restrictions imposed by each application programming interface. The module is connected to the database and does some light parsing on the data it receives. It standardizes the collected data so that it can be saved in a SQL database. The standardization can be done in two ways. If the interface allows than the data is pulled in a pandas data frame, then it is cleaned from unecessary infromation, converted to csv and passed to the database. Otherwise it is parsed as simple text, the data not used will be cleaned, the text will be placed in a csv format and passed to the database.

# Time events Diagram for Data Harvester

![Time Diagram](./Resources Technical Report/time_diagram.png)

# Data usage Legalities

We have consulted the Terms and Conditions for the data we use. After conducting this reasearch we have observed that for the APIs we are using no legal problems could arise. The companies providing the data have full control over what data they are releasing because of that everybody is compling with their requirements automatically.

# Framework

We have used the django framework without the ORM, in order to have complete control over our data processing. This decision was made because we prefer a batteries-included approach to web-application making while we prefer a bare-metal full control type of approach to data management. [citation needed]

# Frontend

The attached wire frame will display the base of how the main page will look like. This wireframe model will be implemented using bootstrap like libraries in order to speed up the process. The base of our frontend will be composed of HTML5, CSS and JavaScript. For CSS we have decided to not use pre-processors since it does not provide any substantial advantage. In the case of JavaScript we will use plotting libraries such as plot.ly in order to get attractive graphs. [citations needed]

![Wire Frame](./Resources Technical Report/wireframe.png)

# Activity Diagram (Non-Technical Aspects)

The following diagram contains a typical user interaction with our website.

![Activity Diagram](./Resources Technical Report/act_diagram.png)

# Inter Layer Comunications

Our Inter layer comunications have been based on the principles of *Separation of Concerns*. Going on this idea we have made sure that at each step each layer knows only as much is it needs. The style and presentation is sent to the client machine and then only the client has interactions with it. The Buisness Logic has been placed as a separate module on the web-server and it only has read writes to the financial data on the database. The logic of the Data Harvester is outside of the Django Web-Server and it does not have any connection with any of the website components other than the write acces to the database. [citations needed]

# User interaction process Diagram (Technical Aspects)

![User interaction Diagram](./Resources Technical Report/request_response_cycle.png)

# Initial Risk Assessment

The following section will highlight the risks that may affect the successful delivery of the software product. We have analysed the impact of all risks across three dimensions - likelihood, severity and detectability. The result of this analysis can be summarised in the following risk assessment matrix.

![](./Resources Technical Report//3D_risk_matrix_filled.png)

For additional details and insight into our mitigation strategies, we will cover each risk from most to least impactful.

## Penetration of Established Market

Backtesting is an established practice among both professional and retail investors [citation needed]. We have to convince people of the superiority of our product. It is unlikely that we will convince investors who have purchased a lifetime license for their backtesting tool to switch to our platform. This is why we consider subscription-based tools as our direct competition. Additionally, we believe that competing with backtesting tools developed for institutional investors will be difficult due to our budget constraints. Hence, we are focusing on beating competitors within the market of subscription-based tools for retail investors.

To gain market share, we have identified three key factors we can leverage to build a superior solution. These are:

* Price - We aim to undercut competitors to make switching that much easier.

* UI - Existing tools often look very unappealing. We aim for creating an enjoyable user experience.

* Feature Set - Solutions on the market are either too expensive or limited in functionality (see appendix {appendixNo}). We want to offer an extensive suite of features that attracts investors from different backgrounds.

Metrics for evaluating whether we have delivered on all of the above can be found in section {sectionNo} discussing our evaluation strategy.

## Access to Historical and Live Data

High quality financial data is an expensive good - entire businesses are built on monopolies of access to certain datasets [citation needed]. Additionally, it is much easier to find price data for some asset classes (e.g. equities) than others (e.g. commodities).

Fortunately, our product does not require access to expensive datasets for initial deployment. Since backtesting for investments purposes does not require extremely granular price data (daily is usually sufficient) [citation needed], we can rely on publicly available datasets and APIs. To accommodate for rate restrictions on calls to the latter, we have made our API adapters highly configurable (see section {sectionNo} for a description of our data collection module) such that we would never run into a situation where we exhausted our available calls per day.

Moreover, we are able to aggregate price data for multiple sources for the same asset into a single datapoint in our asset price database. This reduces the effect of noisy data that may be a result of poor data gathering practices by the data providers. As for the availability of commodity price data, we are able to cover the majority of commodities with free data. For those that remain, we are actively exploring a subscription-based model with multiple data providers.

Relying on APIs for providing live data makes us reliant on the uptime of these APIs. If any of them were to stop providing their services, we would have to find a replacement quickly to minimize downtime of our own platform. Thus, as a precaution, we are using at least two data and up to four (where available) providers for every asset live feed. This redundancy will keep our operations running in case one of them stops servicing our requests and gives us enough time to find a replacement.

## Software Library Bugs

Our product relies on multiple popular open-source libraries and frameworks. Although these have been vetted and stress tested by thousands of developers, there is a non-negligible chance that one of these libraries contains an undiscovered bug.

Since our customers rely on the integrity of our data and calculations, a dysfunctional library could potentially lead them to a wrong conclusion about a given portfolio. In the worst case scenario, this might be a decision to invest in assets which are considerably more risky than the customer believes them to be.

Library bugs can be extremely challenging to detect. To mitigate this risk, we have developed a testing strategy which guarantees that our calculation results meet our expectations (see section {sectionNo} for an extensive discussion of our testing strategy).

Finally, it is worth reiterating that we are not providing financial advice and warn our customers to consult with a professional before making any investment decisions as part of our terms and conditions (see section {sectionNo} for a discussion of the legal implications involved in offering our service).

## Lack of Software Engineering Experience

While some of our team members have worked on large software projects as part of an internship, most have little experience in developing a full-fledged software product. Therefore, there is no evidence that we will be able to handle the complexity involved in building Thalia.

A challenge of detecting this risk is that it becomes apparent only as development of the product progresses and complexity increases. To combat this risk, we are hosting regular retrospective meetings [insert some agile citation covering retros]. These give each team member the chance to go over issues they've run into during the last sprint. This allows us support those struggling in the development process by providing additional training or assissting them through pair programming [citation needed].

## Feature Creep

The number of additional features that could be implemented on top of the core functionality is very large (see appendix {appendixNo} for a full list of all optional features), which risks both overcomplicating the product and shifting the focus from core functionalities to extensions.

We have identified two key strategies for limiting feature creep: preventing a feature with low utility from being developed and pruning features which are rarely used [citations needed]. The former can be implemented by asking our customers for features they would like to see added to Thalia. Commonly requested features would then be discussed by the team with a vote serving as a decision mechanism for whether it should be implemented. Decisions on which features to prune is a matter of collecting usage statistics. For example, a customer will have to activate the display of a non-standard performance metric via the settings menu (an action we can track in anonymized fashion). This allows us to gain insight on the popularity of any given feature after it has been deployed.

## Cloud Hosting Provider Attack Vectors

TODO: Most relevant attack vectors and strategies for mitigation

## Lack of Domain Knowledge

The majority of team members has had little exposure to the domain knowledge required for building parts of our product. A misunderstanding could lead to incorrect implementation of a feature which would put us at risk of being unable to keep up with our schedule.

This risk is entirely internal to our operations and thus more easily controlled. To combat the isolation of knowledge in some members, we have hosted workshops that help spread it to those with little experience in financial markets. Additionally, each member has done extensive reading on topics that concern backtesting in a non-trivial way. Lastly, our regular retrospective meetings require each team member to report their progress over the last sprint. Potential issues concerning misunderstandings or confusion over domain knowledge can thus be spotted early enough to avoid any negative knock-on effects.

## Time Constraints

As for any project, tight deadlines can negatively affect the quality of the end result [citation needed]. Since this product is developed within the scope of a university course, the time each member can allocate to its development is affected by a variety of external factors.

Consequently, we have based our schedule and any estimates on a conservative amount of time each member has to commit to the project to allow for successful delivery (8 hours per week). This gives us confidence in being able to deliver a working product that passes our quality checks in the evaluation stage. If required, we may adjust the schedule by reducing the time spent on developing optional features towards the end of the semester and prioritise core deliverables instead. Hence, we are minimising the likelihood of having to rush development in fear of being unable to meet the deadline otherwise.

## Team Member Dropout

As reported by our supervisor, it is possible (although unlikely) that members of the team drop out of the course due to unforeseen circumstances. A reduced headcount puts us at risk of being unable to meet the requirements and could result in loss of product knowledge if it were to be isolated in the person who dropped out.

Preventing this issue altogether is impossible. However, you can minimise the damage it may cause to the development of the project. The egalitarian team structure (see section {sectionNo}) maximises our 'bus factor', which is a measure of the number of people who would have to stop working on the project to cause development to stall [citation needed]. Every team member is familiar with the code underlying other parts of the product which are outside the scope of his weekly development efforts. Nevertheless, we would have to organise emergency meetings to discuss the impact of such a situation as it arises.

## Software Version Control Hosting

Security breaches involving SVN hosting providers such as GitHub are not unheard of [https://techcrunch.com/2017/11/21/uber-data-breach-from-2016-affected-57-million-riders-and-drivers/]. Rest TODO.

# Initial Project Plan

## Team Organisation

Our workflow is centred around the GitHub platform and the tools it provides such as a ticketing system, pull requests and a scrum board for ongoing tasks. Our goal is not to have fixed responsibilities in our team, so that everybody at some point will be required to develop a feature for each part of the system. Studies have also shown that any sort of status difference within a team can distort the error-correcting mechanism. [[https://absel-ojs-ttu.tdl.org/absel/index.php/absel/article/view/2208/2177](https://absel-ojs-ttu.tdl.org/absel/index.php/absel/article/view/2208/2177)]. Because of these reasons we have decided to commit ourselves to the Egalitarian Team structure, which will introduce the required amount of flexibility into our team.

On the other hand, this also save us from introducing any sort of artificial hierarchy into our development process. Consequently, every team member is guaranteed to have a holistic understanding of how the system works across all layers.

To measure productivity, we use effort-oriented metrics, and assign story points to each ticket, based on the time needed and the functionality of the task. This is done by the team member that the ticket was assigned to, and is later reviewed by another member. As in many Agile teams, story points are based on numbers of the Fibonacci sequence, which forces us to consider the value of each ticket carefully and motivates splitting it into two separate tasks if necessary [[https://www.atlassian.com/agile/project-management/estimation](https://www.atlassian.com/agile/project-management/estimation)].

## Evaluation Strategy and Testing

We also plan to make use of the tools offerred by GitHub for testing and reviewing. Each pull request is reviewed by other team members before any changes are pushed to the production system. CI scripts are also in place to ensure the code quality and integrity, this is done by enforcing the use of Pytest, and a style-checker, either flake-8 or black.

We will also heavily depend on continuous user testing through development [[https://www.system-concepts.com/insights/tips-for-integrating-user-testing-into-an-agile-development-process/](https://www.system-concepts.com/insights/tips-for-integrating-user-testing-into-an-agile-development-process/)]. Our plan is to obtain the necessary ethical approval from the university before the start of development. Continuous user testing is our main part of the evaluation strategy, and as such it will help us to develop features unlike or better than existing ones. This is of key importance as we are about to enter an established market and we would like our product to be as distinguishable as possible.

## Budget

As we are developing this product as part of a university module, we do not have any budget restrictions other than time. All of us are committed to allocating a minimum of 10 hours per week to development efforts and are willing to go beyond that if needed. In order to ensure that we are up to schedule, weekly meetings will be held, which allow the adjustment of workload.

## Milestones

Although agile methods offer a great amount of flexibility, they do require some sort of governance [https://www.agilest.org/agile-project-management/governance/]. For this reason we introduced some important milestones, which will help us to stay on track. We have identified three milestones in the development process, with the last one being much more open ended than the first two, due to the nature of our product. These are the following:

### Minimum Viable Product

This version enables an investor to create a portfolio from a core set of assets and plot its performance versus a predetermined indexing strategy. Since this is not a prototype but a functional product, all future development will expand on this codebase by adding additional features.

### MVG Release 1.0

As defined in our whitepaper, we strive to support five key use cases upon release of our public release of Thalia. Hence, this requires the following features to be fully functional:

- Creating a portfolio from a large set of assets drawn from the major asset classes using input forms.

- Weighing assets relative to each other by assigning a percentage to them using a range input.

- Plotting of a portfolio's performance over a time series upon user request.

- Selection of one of multiple indexing strategies and lazy portfolios from a drop-down list.

- Display of key metrics in a table.

- Specification of regular contributions and selection of a rebalancing interval through input forms.

We consider reaching this milestone as sufficient for the scope of this course.

### Development of Additional Features

If time permits and development goes as planned, we have an array of additional features that we would like to see included in our product. As an example, and also the first of these features, we would like to add exportability to portfolios, allowing users to share their strategies, via a link or a downloadable PDF. For an overview, please have a look at appendix X.

## Schedule

Long-term planning is just as important in Agile development as in alternative planning procedures [[https://www.atlassian.com/agile/product-management/roadmaps](https://www.atlassian.com/agile/product-management/roadmaps)]. As this term we had a chance to set up the working environment and measure the velocity of development, we can make a prediction of the schedule. During the second semester, we will have a total of 12 weeks for developing the product. As we are following the Agile approach, we have divided the schedule according to milestones.

Each one of these periods will include the development of some or multiple features, as well as testing and deployment, leaving us with a fully functional product. The scope for each milestone is defined as follows:

- Week 4 - Closed Beta:

- Key metrics

- Integration of historical datasets

- Additional benchmarks

- Week 8 - Open Release:

- Creating user accounts

- Integration of live data APIs

- Contribution and Rebalancing

- Week 12 - Launch:

- Exporting portfolio

- Additional Features

As previously stated, we aim at including a number of additional features in order to better distinguish our product. The following is a product roadmap based on this schedule:

![](./Resources Technical Report/roadmap.png)

# Proof of Concept

TBD

# Appendices

## Appendix A - Optional Features

- Choose which currency to display values in

- Receive warnings on backtest may be ovefitted to timeframe

- System should not itself handle payments

- Pay for subscription

- Use leverage

- Set upper and lower bound on asset price at which to buy or sell a specific asset

- Warn user about lack of historical data or short timeframe selected

- Flagging market moving events

- Support for Technical Analysis Patterns

- Scripting Language

# References

[1] [Loading times for mobile users]([Google Data, Global, n=3,700 aggregated, anonymized Google Analytics data from a sample of mWeb sites opted into sharing benchmark data, March 2016.])

[2] [Architecture types](IEEE Software 2006 Vol. 23 Issue No. 02 -March/April. Particularly *Software Architecture-Centric Methods and Agile Development*)

[3] [Security guidelines](https://www.ncsc.gov.uk/guidance/separation-and-cloud-security)
