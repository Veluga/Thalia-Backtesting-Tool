# How We Made The Thing

## Technologies

The main programming language of our project is Python. We used Flask and Bulma to make a lightweight, reactive website and Dash to make the main backtesting functionality available as a single-page application.

We developed an in-house library based around pandas for analysing financial data, which covers the major metrics you would care about when backtesting. You can expect to see this extended further to support more advanced metrics for power-users.

Our financial database is kept up-to-date with a module known as the Data Harvester. It regularly collects stock prices from a wide range of sources, normalises and formats them properly, before sending them to our system.

## Process

Our process was based on the Agile methodology. We had weekly meetings in which we reviewed the previous week's work and decided what needed to be done this week (_reword_). We evaluated the difficulty of tasks ourselves before picking our own work. When developing a new module, the team member was responsible for both the implentation and designing the API. Meetings also included retrospectives to find and fix faults in the process. Relatively short sprints of one week meant that we were able to identify unexpected obstacles before they had any long-term impact.  
(_For prose, this feels very bullet-point-y. Suggestions?_)

Each member aimed to average a 10-hour work week to strike a balance between stagnation and burnout. This didn't just include time spent programming, but also writing documentation, attending meetings, reviewing others' code, and self-learning.

Our code is hosted on a private GitHub repositary, with the exception of security-sensitive information. We avoided regression by using continuous integration to run all tests on every push, and maintained a high standard of code-quality with strict reviews.

## To Add

+ Weekly sprints => splitting up work into small pieces.

+ (follow industry standards)

+ Egalitarian:

  + Decisions made as a team, not dictator.

+ (new person mid-project)
