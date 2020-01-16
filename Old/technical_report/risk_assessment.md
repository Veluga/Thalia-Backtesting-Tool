# Initial Risk Assessment

The following section will highlight the risks that may affect the successful delivery of the software product. We have analysed the impact of all risks across three dimensions - likelihood, severity and detectability. The result of this analysis can be summarised in the following risk assessment matrix.

![](/Users/albert-private/Desktop/Desktop/Uni/Year 3/Winter Semester/Software Engineering/Portfolio-backtesting/technical_report/Resources/3D_risk_matrix_filled.png)

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
We have identified two key strategies for limiting feature creep: preventing a feature with low utility from being developed and pruning features which are rarely used [citations needed]. The former can be implemented by asking our customers for features they would like to see added to Thalia. Commonly requested features would then be discussed by the team with a vote serving as a decision mechanism for  whether it should be implemented. Decisions on which features to prune is a matter of collecting usage statistics. For example, a customer will have to activate the display of a non-standard performance metric via the settings menu (an action we can track in anonymized fashion). This allows us to gain insight on the popularity of any given feature after it has been deployed.

## Cloud Hosting Provider Attack Vectors

TODO: Most relevant attack vectors and strategies for mitigation

## Lack of Domain Knowledge

The majority of team members has had little exposure to the domain knowledge required for building parts of our product. A misunderstanding could lead to incorrect implementation of a feature which would put us at risk of being unable to keep up with our schedule.
This risk is entirely internal to our operations and thus more easily controlled. To combat the isolation of knowledge in some members, we have hosted workshops that help spread it to those with little experience in financial markets. Additionally, each member has done extensive reading on topics that concern backtesting in a non-trivial way. Lastly, our regular retrospective meetings require each team member to report their progress over the last sprint. Potential issues concerning misunderstandings or confusion over domain knowledge can thus be spotted early enough to avoid any negative knock-on effects.

## Time Constraints

As for any project, tight deadlines can negatively affect the quality of the end result [citation needed]. Since this product is developed within the scope of a university course, the  time each member can allocate to its development is affected by a variety of external factors.
Consequently, we have based our schedule and any estimates on a conservative amount of time each member has to commit to the project to allow for successful delivery (8 hours per week). This gives us confidence in being able to deliver a working product that passes our quality checks in the evaluation stage. If required, we may adjust the schedule by reducing the time spent on developing optional features towards the end of the semester and prioritise core deliverables instead. Hence, we are minimising the likelihood of having to rush development in fear of being unable to meet the deadline otherwise.

## Team Member Dropout

As reported by our supervisor, it is possible (although unlikely) that members of the team drop out of the course due to unforeseen circumstances. A reduced headcount puts us at risk of being unable to meet the requirements and could result in loss of product knowledge if it were to be isolated in the person who dropped out.
Preventing this issue altogether is impossible. However, you can minimise the damage it may cause to the development of the project. The egalitarian team structure (see section {sectionNo}) maximises our 'bus factor', which is a measure of the number of people who would have to stop working on the project to cause development to stall [citation needed]. Every team member is familiar with the code underlying other parts of the product which are outside the scope of his weekly development efforts. Nevertheless, we would have to organise emergency meetings to discuss the impact of such a situation as it arises.

## Software Version Control Hosting

Security breaches involving SVN hosting providers such as GitHub are not unheard of [https://techcrunch.com/2017/11/21/uber-data-breach-from-2016-affected-57-million-riders-and-drivers/]. Rest TODO.