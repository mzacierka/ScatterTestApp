ECHO Activating virtual environment

venv\Scripts\activate.bat

set FLASK_APP=FlaskAPP

set FLASK_ENV=development

ECHO set environment variables

ECHO Starting Webserver on port  \n

flask run

PAUSE