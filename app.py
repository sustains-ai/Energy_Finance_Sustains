"""
Energy Finance Application
A tool for financial analysis of energy projects with a focus on solar power.
"""

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Database Base class
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-key-for-development-only")

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///energy_finance.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Create all tables
    with app.app_context():
        db.create_all()

    # Main Pages
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/upload")
    def upload():
        return render_template("upload.html")

    @app.route("/analysis")
    def analysis():
        return render_template("analysis.html")

    @app.route("/visualization")
    def visualization():
        return render_template("visualization.html")

    # Project Pages
    @app.route("/projects/import")
    def import_project():
        return render_template("projects/import.html")

    @app.route("/projects/list")
    def list_projects():
        return render_template("projects/list.html")

    @app.route("/projects/new")
    def new_project():
        return render_template("projects/new.html")

    @app.route("/projects/view")
    def view_project():
        return render_template("projects/view.html")

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500

    return app

# Run the app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
