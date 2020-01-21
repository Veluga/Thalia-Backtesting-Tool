# start.sh

# export FLASK_APP=wsgi.py
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=developmentexport
export APP_CONFIG_FILE=config.py

source .envrc
flask run
