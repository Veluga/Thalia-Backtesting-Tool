# Plan for writing validation section of 2nd term Technical Report


## Initial Observations:
- Previous years reports tend to bunch validation in with testing, and spend relatively
little time talking about validation of individual requirements.
- Ernesto specifically points out the importance of validating nonfunctional requirements
on the assessment page

- I would say we do at least some user testing, as this helps justify the more subjective  non functional requirements. According to the lectures validation is also supposed to be about the users perspective. I would recommend creating a short questionnaire ranking things like usability from 1 to 5 and giving it to the people from last term. We would
also have to mention that we did not have access to all user profiles in report.

## Proposed structure and content

### 1. Evaluation of Software quality assurance and Software Quality Control measures
I think it could be good to mention something about how good process leads to
good outcomes. Specifically in terms of the ISO9001 family of standard. I suggest
we write about how we could have a professional QMS audit in the future when we've grown as a company, but also speak about how our current approach emphasizes quality of process.

I would also wax poetic about measures we took to control software quality
that might not have been mentioned previously, specifically code review, refactoring,
cursory mention of tests, focus on knowledge transfer and all the additional documentation
we created for internal use.

### 2. Evaluation
#### Functional requirements
Needs feature lock, talk about what requirements weren't fulfilled and why we
decided not to prioritize them for each.

#### Non Functional requirements
Write a sentence of two for each category explaining how we were able to
verify weather or not our software fulfills a specific functional req.

*I think it is fair to justify not doing some of based on our software being just a prototype*

Usability:
- The product must be easily usable for users who already have some financial investment experience.
*Some limited user testing would be usefull here*
- The basic backtesting interface needs to look familiar to people already experienced with it.
*Either list out similarities to portfolio visualizer: our main competition or do some other kind of justification*
- The product must have detailed instructions on how to use its advertised functions.
*Mention user manual if we're making one and how to on webpage*
- All major functions must be visible from the initial landing page.
*They either is or they isn't*
- Must work in both desktop and mobile browsers.
- The results page should scale with mobile.
*They do or they dont. Maybe could have an image here to ilustrate*

Reliability:
- The product must have a greater than 99\% uptime.
*explain why AWS hosting good and what guarantees they offer*
- All our assets need to have up to date daily data where the asset is still publicly tradeable.
*If the harvester is done we explain that it has been well tested and works subject
to availability on the side of the API*
- All assets supported by the system must provide all publicly available historical datPerformance:
*Harvester does this automatically for supported APIs and assets I believe*
- The website should load within 3 seconds on mobile [2].
*We could use google lighthouse*
- Large portfolios must be supported - up to 300 different assets.
*TBD in person, I think here we have to admit our approach is unwieldly at that scale*

Implementation:
The system needs to work on a cloud hosting provider.
*Id does*

Interfacing:
- The Data Gathering Module must never use APIs stated to-be-deprecated within a month
*this is not something relevant to the prototype*
- The Data Gathering Module must not exceed its contractual usage limits.
*I believe George documented API limits *

Operations:
- An administrator on-call will be necessary for unexpected issues.
*This is definately not something for the prototype*

Packaging:
- The product needs to work inside a Linux container (e.g. Docker).
*I believe it does this*
- All dependencies need to be installable with a single command.
*Here we can talk about development dependencies and whichever of the two requirements lists will eventually be included*

Legal:
*Mention we will have a crack team of lawyers for the finished thing*
- All user testing must be done with ethical approval from the University.
*We spoke to Ernesto and Nigel and they both said this wasn't neccesary*
- UI must display a clear legal disclaimer about the service not providing financial advice.
*I believe its there, would be good if we could find similar disclaimer somewhare else to
evidence that it is adequate*
- All third-party code should allow for commercial use without requiring source disclosure (e.g. no GPL-3).
*I believe this has been done. TBD*
- User data handling should comply with GDPR.

- Provided services should not constitute financial advice under UK law to avoid being subject to financial advice legislation and potential liability.
*same as first point*

Accessibility
- Display items should be clearly labeled.
*Subjective, user testing would be helpful*
- UI should scale to accommodate different screen sizes and aspect ratios,
*It does this, maybe talk about how*
- UI elements and text superimposed over one another should have high contrast in their colors.
*Talk about our color scheme and how we tOtAlLy chose it for this reason*
- UI should allow for the use of assistive technologies to accommodate individuals with accessibility issues.
*Find most popular assistive tech that reads out text and test it with our website,
also mention how elements scale for blind or near sighted people.*

### 4. Evaluation results
- Mention how we fulfill the majority of requirements
- Mention what we could change going forwards in terms of non functionals
- Mention speed and performance optimizations, and potentially other requirements
we could fulfill better
