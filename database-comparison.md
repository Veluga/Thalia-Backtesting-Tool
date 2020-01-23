# REPORT: COMPARISON OF POTENTIAL DBMS SOLUTIONS [INTERNAL USE]
## Arthur-Louis Heath, George Stoian 22.2.20


## EVALUATING REQUIREMENTS
The following are requirements identified for data we must store, a suitable DBMS would ideally satisfy all of these:

Requirements DBMS must scale to meet (Scalability requirements):
1. handle storing a large amount of data
2. acomodate our relatively simple database schema
3. high volume of reads
4. low volume of writes (under once a day per asset)
5. Must be able to handle high volume of concurrent accesses
6. Shoud be cross platform (Since we dont know what platform app would eventually be deployed on)

NOTE: Since we probably won't actualy be deploying Thalia, scaling is a theoretical not practival concern. Since SQLAlchemy supports most popular DBMS, it would also be relatively easy to migrate to a different one during deployment, another reasons requirements during development outweigh requirements during deployment. For these reasons efficiency and scalability weigh less as considerations.


Requirements for development team (Usability requirements):
1. Must be easy to share among multiple machienes (each dev will work on own machiene)
2. Must be easy enough for team members with no prior experience to pick up the basics of in a few days (Easy to learn and deploy)
3. Must be supported by SQLAlchemy (we might be using this as out ORM)
4. have high adoption rate in industry (experience working with DBMS valuable)

Additional requirements for good DBMS:
2. Security (Must be adequatly secure as user data may be sensitive, not important since probably wont be remote accessing)
3. Cost (Must be free to use, must not empose any licensing restrictions on rest of software, not a problem since many of the most popular dbms are FOSS-ish)

## DBMS CONSIDERED
DBMS considered based on articles ranking popular choices from 2019/2020, with ones that failed to reach key requirements, weren't free to use, or had low market adoption excluded.

- **SQLITE**
Pros:
 - Lightweight
 - Good performace
 - Serverless (Instant set up + no configuration necessery)
 - Commonly used for development and testing
 - File based system makes it portable (at least during development when DB not too large)
 - concurrent accesses actually not a problem if only reads (up to 100k page views a day is the common consensus)

Cons:
 - Team expressed wish to work with 'more serious' database application
 - Is not serious in sense that it is not made for large scale applications (might be problems down the line?)
 - No network access (shouldnt be a problem for web app)
 - Shouldnt be used for large apps as it is not developed for this and we would probably encounter problems


Note: If we used SQLite it would mean we would be planning to switch to a DBMS designed for large applications later on, and should be able to JUSTIFY this decision. Miko said he believed this strategy to be silly, as it might cause migration issues. If we use raw SQL queries this is true, if we use SQLAlchemy not so much, as it should be plug and play.

- **POSTGRESQL**

Pros:
 - based and open sourced
 - free
 - can handle metric shitones of data
 - amazing concurrency support
 - is on the rise (people prefer to mySQL)
 - is well positioned to continue going up (no issue with ownership like mySQL)
 - json support is fun (probably doesnt matter for us though)

Cons:
 - Less well doccumented than MySQL
 - Perfromance at its worst in similar use case (doesn't handle large rows and columns well)

- **MYSQL**

Pros:
 - Based and open sourced
 - free
 - very popular
 - many 'engines' and modules to add if desired
 - supported by oracle I guess
 - lots of reasources

Cons:
 - Scales badly (bad performace)
 - popularity in decline
 - some 'down the line' features a pain to set up (incremental backups)

 - **MARIADB**

Pros:
 - based and open sourced (but fully, community driven and no proprietary modules)
 - Many people advocate choosing over MySQL if no license purchased

Cons:
 - easy to migrate to from MySQL not the other way around though
 - not all platforms
 - not really a good reason to use over more popular MySQL

Several other DBMS suitable for large servers were also looked at, but there seemed to not be much of a reason for using these over MySQL or Postgres beyond specific novel (usually advanced) features, that are unlikely to apply to our project or start cosing money beyond a specific performance cap. These were therefore not considered in depth.

## CONCLUSIONS

Depending on weather or not we will be employing raw SQL queries, I would sugjest using SQLite of Postgres. SQLite in the case where we are using SQLAlchemy, as it is portable, light and easy to learn, therefore best suited for use in a development environment, and we could easily scale our app by switching to a different server later on. In the case of writing raw SQL queries (where migration later on is an issue) we would sugjest going with Postgres, as it is more likely to be relevant in our careers, has clearer licensing (compared to mySQL where the extensions are messy af), and has good performance. Although it is less mature/well documented than MySQL, there should be more than adequate doccumentation available for our purposes. It is woth noting that for a database as simple as the one we need, there is not much difference between major DBMS, as they mostly compete on their advanced features. Therefore differences in available documentation, usefull features and even performacne are relatively minor, even after large scale deployment.

As this is essentially an educational excercise, and taking team preference (team expressed dislike for using SQLite) into consideration, we would reccomend going for the devloper favourite and quickly growing Postgres from the start.

## SOME USEFULL SOURCES

[Exhaustive analysis of competing dbms](https://en.wikipedia.org/wiki/Comparison_of_relational_database_management_systems)

[Benchmarkiing for popular dbms (MySQL vs proprietary solutions)](https://pdfs.semanticscholar.org/3209/b47495d01fa75e5b78c3c9ee2919eb6771ca.pdf)

[Market share comparison w/ trends](https://db-engines.com/en/ranking)

[More competitor analysis](https://www.datanyze.com/market-share/databases)