## Needs to answer:

How we test, how we address QA, testing structure, example test cases (2 for report or more than 2 in appendix).

**Secondarily:**

-   Devised before any code is actually written
    
-   Test items (classes, packages, components, subsystems, interfaces. . . )
    
-   Features to be tested
    
-   Features not to be tested
    
-   Speciﬁc techniques and tools to be used
    
-   Criteria for item pass/fail
    
-   Deliverables (test cases speciﬁcation, logs)
    
-   Managerial organisation (people, tasks, schedules, contingency plans)
    

# Testing plan

## Scope

Our biggest concern is ensuring that the results we show are correct. This means ensuring that we do our calculation on the correct data and the outputed results are correct. To help ensure this below is outlined 3 main areas of concern for our business logic handling.

1.  Ensure that all key metric functions, e.g. Sharpe Ratio, are exhaustively tested.
    
2.  Ensuring the graphical output matches our expectation is also worth testing.
    
3.  External information is correct in other words API data and user input.
    

Not related to our business logic but important non-the-less is ensuring authentication is handled properly. If paying customers lack access or non-paying customers exceed their access priviledges, then we have a serious problem with the monetazation of our product.

Closer to the deployment date, we need to test if the application actually works in a production environment. To minimize the "works on my machine" effect, we will be using a container such as Docker to minimise differences between different development environments and production environment. [1] This also makes deployment much easier with many of the cloud hosting providers (e.g. Amazon Web Services or Microsoft Azure) supporting features for hosting containers directly [2] [3].

## Not in scope

We assume our third-party libraries will work as advertised and as such we won't be testing our third-party libraries code. Testing it would cause a large amount of overhead and would make the project impossible to achieve in our allocated timeframe. To alleviate this we will only use mature libraries with large communities and develop our own code when this is not possible.

## Strategy in brief

To achieve accurate calculation needs make sure that our business logic is as extensively tested as we can. They should be independent from other functions and need to have each line scrutinized. Verify boundary conditions, making sure independent paths return as expected. Checking for portfolio validity should be performed before any financial calculations are performed.

Unfortunately at times we must accept user input into the business logic. This input should be verified to be acceptable for the system and any problematic portfolios should be returned as erronous with an appropriate error message to the user. In most cases we must not assume what the user meant, since we are dealing with money.

Another potentially erronous external input could come from our live data third-party APIs. Although we do carefully select our APIs, we should not blindly trust them. We have the convenience of having alternative sources for live data sources so we can verify our primary data sources output against others. As our live data updated daily, the additional overhead of verifying our data will not affect performance of the UX. We make the assumption that the majority APIs won't have an error at the same time as this would defeat the purpose.

~~## Resources~~

~~Testing will be performed along side code production, so we the system should always be have comprehensive test coverage at all times. The need for integration test will need to be identified by the developer themselves or the code reviewer. For black box testing we expect [see schedule to see].~~

## References

1.  Merkel, Dirk. "Docker: lightweight linux containers for consistent development and deployment." *Linux Journal* 2014.239 (2014): 2.
    
2.  https://aws.amazon.com/docker/#Run_Docker_on_AWS
    
3.  https://azure.microsoft.com/en-gb/services/kubernetes-service/docker/