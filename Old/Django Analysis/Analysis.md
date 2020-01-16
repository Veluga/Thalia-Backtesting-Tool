# Observations

* Routing is done with regexs
* Process of getting started is much more involved than with Flask (i.e. "Hello, World!")
* Projects consist of one or multiple apps which can serve different routes
    * 'Global' urls.py links app urls.py with some route group (may overlap)
* Support for PostgreSQL, MySQL, Oracle and SQLite
* Migrations work just as you'd expect them to - so do Models
* django-admin / manage.py serve as command-line utility for administrative tasks (makemigrations, test, startapp, etc.)
* Built-in views for status 500/400/403, etc.
* Given context (dict-like object), template engine renders template into HTML
* Requests are forwarded to web applications using WSGI (Web Server Gateway Interface)
* Preferred way to write tests is using unittest (but supports any Python testing framework)
* Built-in tools commonly needed (Logging, Cachine, Sessions, etc.)
* There is a debugging toolbar
* There exists a Redis client for Django

# Conclusion

* I can not detect any red flags that would prevent us from using this. It has my approval and I'd even endorse using it, since framework learning overhead should be minimal with this. 
