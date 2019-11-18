# Initial Project Plan

## Team Organisation

Our workflow is centred around the GitHub platform and the tools it provides such as a ticketing system, pull requests and a scrum board for ongoing tasks. Our goal is not to have fixed responsibilities in our team, so that everybody at some point will be required to develop a feature for each part of the system. Studies have also shown that any sort of status difference within a team can distort the error-correcting mechanism. [[https://absel-ojs-ttu.tdl.org/absel/index.php/absel/article/view/2208/2177](https://absel-ojs-ttu.tdl.org/absel/index.php/absel/article/view/2208/2177)]. Because of these reasons we have decided to commit ourselves to the Egalitarian Team structure, which will introduce the required amount of flexibility into our team.

On the other hand, this also save us from introducing any sort of artificial hierarchy into our development process. Consequently, every team member is guaranteed to have a holistic understanding of how the system works across all layers.

To measure productivity, we use effort-oriented metrics, and assign story points to each ticket, based on the time needed and the functionality of the task. This is done by the team member that the ticket was assigned to, and is later reviewed by another member. As in many Agile teams, story points are based on numbers of the Fibonacci sequence, which forces us to consider the value of each ticket carefully and motivates splitting it into two separate tasks if necessary [[https://www.atlassian.com/agile/project-management/estimation](https://www.atlassian.com/agile/project-management/estimation)].

## Evaluation Strategy and Testing

We also plan to make use of the tools offerred by GitHub for testing and reviewing. Each pull request is reviewed by other team members before any changes are pushed to the production system. CI scripts are also in place to ensure the code quality and integrity, this is done by enforcing the use of Pytest, and a style-checker, which is still to be determined.

We will also heavily depend on continuous user testing through development [[https://www.system-concepts.com/insights/tips-for-integrating-user-testing-into-an-agile-development-process/](https://www.system-concepts.com/insights/tips-for-integrating-user-testing-into-an-agile-development-process/)]. Our plan is to obtain the necessary ethical approval from the university before the start of development. Continuous user testing is our main part of the evaluation strategy, and as such it will help us to develop features unlike or better than existing ones. This is of key importance as we are about to enter an established market and we would like our product to be as distinguishable as possible.

## Budget

As we are developing this product as part of a university module, we do not have any budget restrictions other than
time. All of us are committed to allocating a minimum of 10 hours per week to development efforts and are willing to go
beyond that if needed. In order to ensure that we are up to schedule, weekly meetings will be held, which allow the adjustment of workload.

## Milestones

Although agile methods offer a great amount of flexibility, they do require some sort of governance [[https://disciplinedagiledelivery.com/dad-milestones/](https://disciplinedagiledelivery.com/dad-milestones/)]. For this reason we introduced some important milestones, which will help us to stay on track. We have identified three milestones in the development process, with the last one being much more open ended than the first two, due to the nature of our product. These are the following:

### Minimum Viable Product

This version enables an investor to create a portfolio from a core set of assets and plot its performance versus a predetermined indexing strategy. Since this is not a prototype but a functional product, all future development will expand on this codebase by adding additional features.

### MVG Release 1.0

As defined in our whitepaper, we strive to support five key use cases upon release of our public release of
{MVG}. Hence, this requires the following features to be fully functional:

-   Creating a portfolio from a large set of assets drawn from the major asset classes using input forms.
-   Weighing assets relative to each other by assigning a percentage to them using a range input.
-   Plotting of a portfolio's performance over a time series upon user request.
-   Selection of one of multiple indexing strategies and lazy portfolios from a drop-down list.
-   Display of key metrics in a table.
-   Specification of regular contributions and selection of a rebalancing interval through input forms.

We consider reaching this milestone as sufficient for the scope of this course.

### Development of Additional Features

If time permits and development goes as planned, we have an array of additional features that we would like to see included in our product. As an example, and also the first of these features, we would like to add exportability to portfolios, allowing users to share their strategies, via a link or a downloadable PDF. For an overview, please have a look at appendix X.

## Schedule

Long-term planning is just as important in Agile development as in alternative planning procedures [[https://www.atlassian.com/agile/product-management/roadmaps](https://www.atlassian.com/agile/product-management/roadmaps)]. As this term we had a chance to set up the working environment and measure the velocity of development, we can make a prediction of the schedule. During the second semester, we will have a total of 12 weeks for developing the product. As we are following the Agile approach, we have divided the schedule according to milestones.

Each one of these periods will include the development of some or multiple features, as well as testing and deployment, leaving us with a fully functional product. The scope for each milestone is defined as follows:

-   Week 4 - Closed Beta:
    
    -   Key metrics
        
    -   Integration of historical datasets
        
    -   Additional benchmarks
        
-   Week 8 - Open Release:
    
    -   Creating user accounts
        
    -   Integration of live data APIs
        
    -   Contribution and Rebalancing
        
-   Week 12 - Launch:
    
    -   Exporting portfolio
        
    -   Additional Features
        

As previously stated, we aim at including a number of additional features in order to better distinguish our product. The following is a product roadmap based on this schedule:
