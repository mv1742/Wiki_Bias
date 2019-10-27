from flask import Flask
from flask import render_template

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return render_template("homepage.html")
# def create_app():
#     """Construct the core application."""
#     app = flask(__name__,
#                 instance_relative_config=False)
# flask_app.config.from_object('config.Config')
#
# with flask_app.app_context():
#
# # Import main Blueprint
# from ./application import routes
# flask_app.register_blueprint(routes.main_bp)
#
# # Import Dash application
# from ./application/dash_application import dash_example
# flask_app = dash_example.Add_Dash(flask_app)
#
# # from ../dash_nlp import app1
# # app = app1.Add_Dash(app)
#
# # Compile assets
# from ./application/assets import compile_assets
# compile_assets(flask_app)

