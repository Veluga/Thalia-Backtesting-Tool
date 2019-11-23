# Testing plan

## Scope

Our biggest concern is ensuring that the results we show to our users are correct. Outlined below are the main functionalities we need to be especially careful about when we test.

1. Results of  key metric functions, e.g. Sharpe Ratio

2. Data plotting results

3. Handling of third-party API data

4. User authentication

Closer to the deployment date, we need to also test if the application works in a production environment. To minimise the "works on my machine"-effect, we will be using a container such as Docker to minimise differences between different development environments and production environment [1]. This also eases deployment much easier with many of the cloud hosting providers (e.g. Amazon Web Services or Microsoft Azure) since they support hosting containers natively [2] [3].

## Not in scope

We assume our third-party libraries will work as advertised and as such we will not be testing them. Testing them would cause a large amount of overhead and would make the project impossible to achieve in our allocated time frame. To alleviate this, we will only use mature libraries with large communities and develop our own code when this is not possible.

## Strategy in brief

For most of our testing, just employing good testing practices will be enough. All public APIs should have unit tests, all interfacing modules should have integration tests and the most critical code should have extensive tests for different branching paths and boundary checking.

No assumptions should be made about user input since the nature of our application demands rigorous verification of intent. Input should be verified to be acceptable for the system and any problematic portfolios should be returned as erroneous with an appropriate error message to the user.

Another potentially erroneous external input could come from our live data third-party APIs. Although we do carefully select our APIs, we should not blindly trust them. We have the convenience of having alternative sources for live data sources, hence we can verify our primary data sources output against others. As our live data are/is updated daily, the additional overhead of verifying our data will not affect the performance of the UX.

## References

1. Merkel, Dirk. "Docker: lightweight Linux containers for consistent development and deployment." *Linux Journal* 2014.239 (2014): 2.

2. https://aws.amazon.com/docker/#Run_Docker_on_AWS

3. https://azure.microsoft.com/en-gb/services/kubernetes-service/docker/
