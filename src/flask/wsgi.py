"""Application entry point."""
from application import create_app
# from application import routes as homepage
import flask_app
import sys
print(sys.path)
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
app = create_app()
# from app1 import app as app1
# from app2 import app as app2
# from app3 import app as app3
# from .layout import html_layout
# from analytics import app as app4
#
from application.dash_application import dash_example

app_werkzeug = DispatcherMiddleware(app, {
    # '/lda': app1.server,
    # '/app4':app2.server,
    # '/app3':app3.server,
    # '/app4':app4.server,
})
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', debug=True)
# app_werkzeug.register_blueprint(routes.main_bp)

if __name__ == '__main__':
    run_simple('0.0.0.0', 8050, app_werkzeug)

