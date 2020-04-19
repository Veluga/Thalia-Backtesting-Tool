# How We Made The Thing

## Technologies

(I think here it would be good to mention what these technologies are just in case So instead of Flask and Bulma say 
Flask as our web framework and Bulma as our css thingie)

The main programming language of our project is Python. We used Flask and Bulma to make a lightweight, reactive website and Dash to make the main backtesting functionality available as a single-page application.

We developed an in-house library based around pandas for analysing financial data, which covers the major metrics you would care about when backtesting. You can expect to see this extended further to support more advanced metrics for power-users.

(Finda?)

Our financial database is kept up-to-date with a module known as the Data Harvester. It regularly collects stock prices from a wide range of sources, normalises and formats them properly, before sending them to our system.



## Process

Our process was based on the Agile methodology. Our team worked in weekly sprints, starting with a team meeting in which we reviewed the previous week's work and allocated new work to members. Our aim was to keep units of work  small, easy to review and well tested.

To implement an egalitarian team structure, most decisions we're made based on group consensus. Additionally our members we're encouraged not to specialize, but rather to familiarize themselves with all areas of Thalia's development. This offered us great flexibility and resilience when allocating work as team members were essentially interchangeable.

(---- This might be personal preference but I think passive voice to refer the team sounds better))

Additionally members we're encouraged to asses the difficulty of tasks themselves before picking their own work. When developing a new module, the team member was responsible for both the implentation and design of its API.

We ended each meeting with a retrospective, where we aimed to reflect, and try to fix faults in our process. Relatively short sprints of one week meant that we were flexible, being able to identify unexpected obstacles before they had any long-term impact.  

(--- Maybe we should mention that we didn't have specialized roles?)

Each member aimed to average a 10-hour work week to strike a balance between stagnation and burnout. This didn't just include time spent programming, but also writing documentation, attending meetings, reviewing others' code, and self-learning.

Our code is hosted on a private GitHub repositary, with the exception of security-sensitive information. We avoided regression by
(Like, im not sure if 'on every push' is too jargony or not? since its a github specific thing)
 adopting a continuous integration process and fully testing every iteration of our code, and maintained a high standard of code-quality with strict reviews.

## To Add

+ Weekly sprints => splitting up work into small pieces.
(Ive addded my suggestion for this to the text above)


+ (follow industry standards)



+ Egalitarian:
(Ive addded my suggestion for this to the text above)

  + Decisions made as a team, not dictator.

+ (new person mid-project)
At the middle of the project, we we're joined by a new team member, who was returning from their year abroad. It proved to be a challenge to get our new member up to speed on our vision and tools we we're using so that they could begin contributing as soon as possible.


(---- Does one mention evaluation here?)