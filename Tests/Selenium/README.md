# End to end testing with Selenium

## Notes on implementation

- Due to limitations of architecture and CircleCI, end-to-end testing with Selenium must be done localy.
To prevent them from failing on CircleCI the automated tests in this directory do not follow the pytest naming scheme 
of test_*.py and are run with the help of the 'main_test.py' testing script instead of pytest.

- Tests assume Thalia has been run localy and is available at localhost:5000, and that the accompanying test databases 
(financial data and user accounts) are configured correctly.

- Tests are meant to be part of end-to-end testing conducted at end of project, and are sensative to the website's layout.
Since some of the static content of webpages (Eg. text on about page) was not yet finalized at time of writing, this is not tested
automatically but was validated by hand after development finished.

## Running the selenium automated tests



## Notes

Some issues may arise due to page load times (most likely driver address checks will fail). If the tests are being run on a particularly slow system, the page_wait time in util.py can be increased to counteract this issue