# Video Demonstration Script

​
[Homepage]
When we first go to the website, we're presented with this decription page of Thalia.
​
Now, if you're not familiar with backtesting or Thalia, there's a _Learn More_ section if you need it.
​
In order to use Thalia, you need an account. It's very simple to create - you just need a username and password. So let's go ahead and create one real quick.

[Type in username "ThaliaIsCool" and password "LiveLaugh1nvest?"]
There are a few limitations on passwords - you to have need at least one letter, number, and special character; and they need to be at least 8 characters long.
​
[Log in.]

Now that we're logged in, we can go to the _My Portfolio's_ tab.

[Place mouse on link.]
You can see the link in the NavBar right here.

[Click the link.]
This is where you can see and manage all your portfolios. This is a new account, so we don't have any just yet. Let's remedy that by making our first portfolio.
​
To do this, we need to go to the _Dashboard_.
​
[Go to dashboard.]
The first thing we have to do is decide what time period we're interested in. Here, you can see the default is between the 1st of January 1970 and today.
​
The next thing is our _initial investment_. The default here is 1000 dollars. I'm happy with that, so let's go down a little bit.

You can see that the thing below is contribution and rebalancing. We're going to ignore that for just a moment and focus on the more essential part - selecting assets and allocating funds to them.
​​
Let's just pick two assets here, and give 50% to each of them.

[Pick two TBD assets and type 50 next to them in the allocation table.]

Now these numbers here don't need to add up to 100, like percentages. So if I change this 50 to a 30 nothing bad will happen - I'll just have a different allocation. But personally I like percentages, so let's change it back.
​
Coming back up for a moment, if I have an income and want to use it to invest more into my portfolio as time goes on, we can model that here with _contribution_. So let's say I want to put an extra 100 dollars worth into my portfolio every month, I just type 100 here and select _monthy_ here.
​
Over time, it's possible that these assets will go up and down in value differently, so this nice 50-50 split might not stay 50-50 for long. Now, if you've decided that you don't want that, and you'll buy and sell regularly to keep the portfolio at its initial balance, you can model that by selecting a _rebalancing_ frequency.

That's all that goes into _creating_ a portfolio, so let's clear this out and show off lazy portfolios.

[Delete assets from the allocation table. Click on a lazy portfolio.]
​
You can name your portfolios if you want. Let's call this one "My First Portfolio".

[Rename portfolio.]
​
Quite often we want to compare portfolios against each other. To do this, all we have to do is click this button to add a portfolio and fill in the details.
​​
[adds another lazy portfolio]
OR
[Adds a normal portfolio to spend more time]

You can fiddle about with the options here as much as you want, but for now let's actually look at the results of what we've done.

[Click Submit.]
​
After submitting the portfolio or portfolios if more were created the user can go the tabs that have just become available in order to check the backtesting results.​
​
[present_summary]
The summary contains a plot with the total returns overtime followed by some key information extracted from the metrics, returns, drawdowns and assets.
​
If the user wants more details about each one of those he can click on the corresponding tab in order to see the full details.
​
For an in-detail look, we will look at each one of the tabs.
​
[shows key metrics]
The key metrics are presented in the form of a table.
​
[show returns]
For the returns it displays a plot with the yearly differences and table with the annual returns.
​
[show drawdown]
The drawdowns are displayed as a yearly drawdown plot and drawdown table.
​
[show assets]
And in the end a breakdown of the assets that make up the portfolios is given.
​​
After checking how the portfolio or portfolios performs the user can go back to the ticker selection tab in order to tweak the settings. In addition to this he can click on the "Export to PDF" button in order to export the current backtesting results as a PDF.
​​
After multiple rounds of tweaking the risk of overfitting can appear.
​
​As a result, we have added an overfitting checking mechanism.
​
OR
​
This is a scenario where the user has tweaked a portfolio in such a way that it makes a huge profit over an extremely specific period of time. This is something that should be avoided and as a consequence, we have added an overfitting checking mechanism.
​​
If the user wants to check for overfitting he can simply go to the overfitting tab and click on Check Overfitting.  He then is informed if overfitting was detected in any of his portfolios.
​
Now that we have shown a demonstration of our product we will go into the technologies used to create it.
