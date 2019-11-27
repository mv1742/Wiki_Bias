"""Initialize app."""
from flask import Flask
from flask import render_template

def create_app():
    """Construct the core application."""
    app = Flask(__name__,
                instance_relative_config=False)
    app.config.from_object('config.Config')
    @app.route('/')
    def index():
        return render_template("index.html", title='Source of Conflict.',
                           template='home-template',
                           body="Insight Data Engineering NY Project")

    with app.app_context():

        from .dash_application import analytics
        app = analytics.Add_Dash(app)
        from .dash_application import categories
        app = categories.Add_Dash(app)
        from .dash_application import articles
        app = articles.Add_Dash(app)
        # # Import Dash application
        # from .dash_application import dash_example
        # app = dash_example.Add_Dash(app)
        #
        from .dash_application import search
        app = search.Add_Dash(app)
        from .dash_application import timeseries
        app = timeseries.Add_Dash(app)
        # from .dash_application import lda_4
        # app = lda_4.Add_Dash(app)
        from .dash_application import word_cloud
        app = word_cloud.Add_Dash(app)

        # from ../dash_nlp import app1
        # app = app1.Add_Dash(app)
        # Compile assets
        # # from .assets import compile_assets
        # compile_assets(app)

        return app
