# Initial Risk Assessment
The following section will highlight some of the biggest risks that may affect the successful delivery of the software product, ordered by their level of impact. For each case we will first discuss its nature followed by our strategy in mitigating it. Finally, we will see how these scenarios lay out in a simplified 3D risk matrix.

## Critical Cases
### Access to Historical and Live Data
High quality financial data is an expensive good - entire businesses are built on monopolies of access to certain datasets. Additionally, it is much easier to find price data for some asset classes (e.g. equities) than others (e.g. commodities).
Fortunately, our product does not require access to expensive datasets for initial deployment. Since backtesting for investments purposes does not require extremely granular price data (daily is usually sufficient), we can rely on publicly available datasets and APIs. To accommodate for rate restrictions on calls to the latter, we have made our API adapters highly configurable such that we would never run into a situation where we exhausted our available calls per day. Moreover, we are able to aggregate price data for multiple sources for the same asset.
This reduces the effect of noisy data that may be a result of poor data gathering practices by the data providers. As for the availability of commodity price data, we are able to cover the majority of commodities with free data. For those that remain, we are actively exploring a subscription-based model with multiple data providers. Relying on APIs for providing live data makes us reliant on the uptime of these APIs. If any of them were to stop providing their services, we would have to find a replacement quickly to minimize downtime of our own platform. As a precaution, we will try to cover every asset live feed with at least two data providers. This will keep our operations running in case one of them stops servicing our requests.
Furthermore, as our data collector is to run at regular intervals, we would be able to detect the problem early. Given this, and previous precautions, we believe failure in such a scenario would be unlikely.

## Marginal Cases
### Penetration of Established Market
Backtesting is an established practice among both professional and retail investors. We have to convince people of the superiority of our product. It is unlikely that we will convince investors who have purchased a lifetime license for their backtesting tool to switch to our platform. This is why we consider subscription-based tools as our direct competition. To gain market share, we have identified three key factors we can leverage to build a superior solution. These are:
* Price - We aim to undercut competitors to make switching that much easier.
* UI - Existing tools often look very unappealing. We aim for creating an enjoyable user experience.
* Feature Set - Solutions on the market are either too expensive or limited in functionality. We want to offer an extensive suite of features that attracts investors from different backgrounds.

### Software Bugs in Used Libraries
In our development we heavily rely on some already existing libraries and frameworks. Upon selection we investigated all used pieces of software carefully, determining their relevancy and quality. Although we have not checked every line of code of such libraries, we claim that each used piece of software is either, professionally made, community approved or self-tested. As a consequence, the likelihood of this scenario is low, even though it would be considerably challenging to detect. 

### Time Constraints
As for any project, tight deadlines can negatively affect the quality of the end result. Considering that all team members have duties outside of this project, it is important to consider the risk of pressing time constraints. Notwithstanding that, each one of us is committed to spending the necessary hours on the project, including regular meetings and reports, which will allow us to adjust the time needed for development. As the deadlines and the outline of the development schedule is mostly known at present, we assume that the likelihood of a rushed product due to deadlines is low. 

## Negligible Cases
### Lack of Domain Knowledge
The majority of team members has had little exposure to the domain knowledge required for building parts of our product. Other than the aforementioned risks, this risk is entirely internal to our operations and thus more easily controlled. To combat the isolation of knowledge in some members, we have hosted workshops that help spread it to those with little experience in financial markets. Additionally, each member has done extensive reading on topics that concern backtesting in a non-trivial way.
Moreover, as we hold regular meetings, which requires each team member to report about their progress retrospectively, nescience would not go unnoticed, which then could be helped by other team members.
### Feature Creep
Due to the nature of our product the number of possible features that could be implemented is practically endless, which risks both overcomplicating the product and shifting the focus from core functionalities to features. This is due to the fact that some investors like to use uncommon metrics for evaluating their strategies, and that there are several ways of making the backtesting procedure more dynamic and responsive. Nevertheless, as most of these features do not depend on each other, we can work on them separately, and implement only some of them.

## Risk Matrix
To see how these cases are related, consider a 3-dimensional risk matrix, with the three axes being impact, likelihood, and detectability. In order to aid visualization, the third dimension is expressed as a cell colour. The matrix is then as follows:
-----------------------
And with the element in the correct places: 
----------------------
