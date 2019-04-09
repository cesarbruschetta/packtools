# coding:utf-8
import os
from flask import Flask, render_template
from flask_babelex import Babel

from .custom_filters import clean_uri, utility_processor
from .views import main as main_bp




def create_app(settings_ns):

    babel = Babel()
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder="static",
        instance_relative_config=False,
    )

    app.config.from_object(settings_ns)

    from packtools.webapp.views import main as main_bp

    app.register_blueprint(main_bp)

    app.jinja_env.filters["clean_uri"] = clean_uri
    app.context_processor(utility_processor)

    # i18n
    babel.init_app(app)
    # Debug Toolbar
    if app.config["DEBUG"]:
        # Toolbar
        from flask_debugtoolbar import DebugToolbarExtension

        toolbar = DebugToolbarExtension()
        toolbar.init_app(app)

    return app


app = create_app(os.environ.get(
    "APP_SETTINGS", "packtools.webapp.config.default.ProductionConfig"))
