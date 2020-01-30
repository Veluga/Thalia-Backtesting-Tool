# Thalia

Web app for backtesting a portfolio.

## Instruction

### Run the app

To do a fresh install and run Thalia:

```shell
python3 -m venv venv && source venv/bin/activate # setup virtual environment

pip install . # install Thalia

chmod +x start.sh # give start script permission to run

./start.sh # run Thalia
```

### Run tests

To install test dependencies:

```shell
pip install -e ".[test]"
```

To run the tests:

```shell
pytest
```

if you have pytest installed globally you may need to run:

```shell
python -m pytest
```

To install app in active edit mode and Thalia's development dependencies e.g. linter and formater

N.B: quotes are important

```shell
pip install -e ".[dev]"
```

### Test coverage

To see test coverage:

```shell
coverage run --source Thalia -m pytest
```

Then for a quick percentage of lines under test coverage run:

```
coverage report
```

To generate more visual report inside `coverage_html_report`-directory. The report can then be opened in a browser

```
coverage html
```

## Notes

Thalia web forked from https://github.com/okomarov/dash_on_flask
