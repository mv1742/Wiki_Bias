"""Application entry point."""
from application import create_app
# from application import routes as homepage
import flask_app
import sys
print(sys.path)
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
app = create_app()

from application.dash_application import dash_example

app_werkzeug = DispatcherMiddleware(app, {
})


if __name__ == '__main__':
    run_simple('0.0.0.0', 8050, app_werkzeug)

