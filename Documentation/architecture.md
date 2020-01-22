# Architecture

## HIGH LEVEL

The application is split into 3 independent packages. The website 'Thalia', the data collecting module 'Harvester' and the Financial data handling library 'BL' (temp name). Tests share a 'Test' directory.

The coupling should be limited to the following two exceptions:

1. A shared ticker data schema for Thalia and the Harvester.
2. A shared data format API between BL and Thalia.

## DESIGN DECISIONS

We have this separation so all 3 modules are independent i.e. for maximum cohesion and minimum coupling. So the only change is BL is now a library agnostic from the web app.

## Flask Architecture

We separate modules by function i.e. templates in one directory, views in another, etc. BL

So code that communicates with the Database is placed in models under in a file responsible for their behavior e.g. user table handling is placed in user.py. Same for templates and views.

example functional based structure from [blog post](https://lepture.com/en/2018/structure-of-a-flask-project)

```
Thalia/
  __init__.py
  views.py
  Models/
    __init__.py
    example.py
    example.py
    ...
  Templates/
    example.html
    example.html
    ...
  Dash/
    example.py
    example.py
  Static/
    example.css
    example.html
    example.jpg
```

exception exists for the main dashboard, which will be entirely handled by Dash.

## ARCHITECTURE DOCUMENATION

Going folder by folder:

- `BL` contains the library for all numerical calculation used on the raw data
  - Internals undecided
- `Harvester` contains the module for pulling financial data from APIs and placing it in the Database. N.B. does not interact with other code
  - Each file is it's own API handler
    - Handles initial seeding and daily updates
- `Tests` contains tests for all modules
- `Thalia` contains Thalia web, i.e. the Flask app.
  - Already discussed above
