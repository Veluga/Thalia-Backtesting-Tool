base_html = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Thalia - Dashboard</title>
        <link rel="shortcut icon" href="../../static/favicon.ico">
        {%css%}
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css"/>
        <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
        <script src="../static/scripts/export-pdf.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/1.5.3/jspdf.debug.js" integrity="sha384-NaWTHo/8YCBYJ59830LTz/P4aQZK1sS0SneOgAvhsIl3zBu8r9RevNg5lHCHAuQ/" crossorigin="anonymous"></script>
        <style>
        .is-inspire:after {
            border-color: #f26a4b !important;
        }
        </style>
    </head>
    <body>

        <nav class="navbar" role="navigation" aria-label="main navigation" onclick="document.querySelector('.navbar-menu').classList.toggle('is-active');">
        <div class="navbar-brand">
        <a class="navbar-item" href="/">
            <img src="/static/images/Logos/large_logo.png" width="128" height="64">
        </a>

        <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
        </a>
        </div>

        <div id="navbarBasicExample" class="navbar-menu">
        <div class="navbar-start">
            <a href="/" class="navbar-item">
            Home
            </a>
            <a href="/about/" class="navbar-item">
            About
            </a>
            <a href="/gallery/" class="navbar-item">
            My Portfolios
            </a>
            <a href="/dashboard/" class="navbar-item">
            Dashboard
            </a>
            <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link is-inspire">
                More
            </a>
            <div class="navbar-dropdown">
                <a class="navbar-item">
                Contact
                </a>
                <hr class="navbar-divider">
                <a href="/contact/" class="navbar-item">
                Contact Us
                </a>
            </div>
            </div>
        </div>

        <div class="navbar-end">
            <div class="navbar-item">
            <div class="buttons">
                <button class="button is-white" onclick="exportPDF()"> Export to PDF </button>
                <button class="button is-white" disabled></button>
                <a href="/logout/" class="button is-white">
                Log out
                </a>
            </div>
            </div>
        </div>
        </div>
    </nav>

        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div></div>
    </body>
</html>
"""
