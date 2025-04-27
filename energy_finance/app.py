"""
Energy Finance Application
A tool for financial analysis of energy projects with a focus on solar power.
"""

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-for-development-only")

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///energy_finance.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models after db initialization
from energy_finance.models.project import Project, SolarProject
from energy_finance.models.financial import CashFlow, FinancialMetric

# Create database tables
with app.app_context():
    db.create_all()

# Import routes
from energy_finance.routes import main_routes, project_routes, analysis_routes

# Register blueprints
app.register_blueprint(main_routes.main_bp)
app.register_blueprint(project_routes.project_bp, url_prefix='/projects')
app.register_blueprint(analysis_routes.analysis_bp, url_prefix='/analysis')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')