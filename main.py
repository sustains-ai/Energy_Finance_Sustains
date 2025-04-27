"""
Energy Finance Application - Main Entry Point
This is the main entry point for the Energy Finance application.
A powerful tool for financial analysis of energy projects with a focus on solar power.
"""

import os
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import create_app, db
from models import Project, SolarProject, CashFlow, FinancialMetric

# Create the Flask application
app = create_app()

# Configure file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set a secret key for flash messages
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key_for_energy_finance")

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Register routes
@app.route('/')
def index():
    """Home page of the Energy Finance application"""
    return render_template('index.html')

@app.route('/projects')
def list_projects():
    """List all projects"""
    projects = Project.query.all()
    return render_template('projects/list.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    """Create a new project"""
    if request.method == 'POST':
        try:
            # Extract basic project information
            name = request.form.get('name')
            project_type = request.form.get('project_type')
            description = request.form.get('description')
            location = request.form.get('location')
            capacity_mw = request.form.get('capacity_mw')
            status = request.form.get('status', 'planning')
            
            # Extract financial information
            capex = request.form.get('capex')
            capex_per_mw = request.form.get('capex_per_mw')
            opex_per_year = request.form.get('opex_per_year')
            opex_per_mw = request.form.get('opex_per_mw')
            
            # Extract timeline information
            start_date_str = request.form.get('start_date')
            commercial_operation_date_str = request.form.get('commercial_operation_date')
            expected_lifetime_years = request.form.get('expected_lifetime_years', 25)
            
            # Convert string dates to date objects if they exist
            start_date = None
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                
            commercial_operation_date = None
            if commercial_operation_date_str:
                commercial_operation_date = datetime.strptime(commercial_operation_date_str, '%Y-%m-%d').date()
            
            # Create a new project based on type
            if project_type == 'solar':
                # Extract solar-specific information
                panel_type = request.form.get('panel_type')
                panel_efficiency = request.form.get('panel_efficiency')
                num_panels = request.form.get('num_panels')
                panel_capacity_w = request.form.get('panel_capacity_w')
                latitude = request.form.get('latitude')
                longitude = request.form.get('longitude')
                tilt_angle = request.form.get('tilt_angle')
                azimuth = request.form.get('azimuth')
                degradation_rate = request.form.get('degradation_rate', 0.5)
                performance_ratio = request.form.get('performance_ratio', 0.75)
                land_area_acres = request.form.get('land_area_acres')
                tracking_type = request.form.get('tracking_type', 'fixed')
                
                # Create a new solar project
                project = SolarProject(
                    name=name,
                    description=description,
                    location=location,
                    capacity_mw=float(capacity_mw) if capacity_mw else None,
                    project_type=project_type,
                    status=status,
                    capex=float(capex) if capex else None,
                    capex_per_mw=float(capex_per_mw) if capex_per_mw else None,
                    opex_per_year=float(opex_per_year) if opex_per_year else None,
                    opex_per_mw=float(opex_per_mw) if opex_per_mw else None,
                    start_date=start_date,
                    commercial_operation_date=commercial_operation_date,
                    expected_lifetime_years=int(expected_lifetime_years) if expected_lifetime_years else 25,
                    panel_type=panel_type,
                    panel_efficiency=float(panel_efficiency) if panel_efficiency else None,
                    num_panels=int(num_panels) if num_panels else None,
                    panel_capacity_w=float(panel_capacity_w) if panel_capacity_w else None,
                    latitude=float(latitude) if latitude else None,
                    longitude=float(longitude) if longitude else None,
                    tilt_angle=float(tilt_angle) if tilt_angle else None,
                    azimuth=float(azimuth) if azimuth else None,
                    degradation_rate=float(degradation_rate) if degradation_rate else 0.5,
                    performance_ratio=float(performance_ratio) if performance_ratio else 0.75,
                    land_area_acres=float(land_area_acres) if land_area_acres else None,
                    tracking_type=tracking_type
                )
            else:
                # Create a generic project for other types (will be expanded later)
                project = Project(
                    name=name,
                    description=description,
                    location=location,
                    capacity_mw=float(capacity_mw) if capacity_mw else None,
                    project_type=project_type,
                    status=status,
                    capex=float(capex) if capex else None,
                    capex_per_mw=float(capex_per_mw) if capex_per_mw else None,
                    opex_per_year=float(opex_per_year) if opex_per_year else None,
                    opex_per_mw=float(opex_per_mw) if opex_per_mw else None,
                    start_date=start_date,
                    commercial_operation_date=commercial_operation_date,
                    expected_lifetime_years=int(expected_lifetime_years) if expected_lifetime_years else 25
                )
            
            # Add and commit the new project to the database
            db.session.add(project)
            db.session.commit()
            
            # Flash a success message
            flash(f"Project '{name}' created successfully!", "success")
            
            # Redirect to the project view page
            return redirect(url_for('view_project', project_id=project.id))
        
        except Exception as e:
            # If there's an error, roll back the database session and flash error message
            db.session.rollback()
            flash(f"Error creating project: {str(e)}", "danger")
            return render_template('projects/new.html')
    
    return render_template('projects/new.html')

@app.route('/projects/import', methods=['GET', 'POST'])
def import_project():
    """Import a project from CSV or Excel file"""
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'projectFile' not in request.files:
            return render_template('projects/import.html', error="No file provided")
        
        file = request.files['projectFile']
        if file.filename == '':
            return render_template('projects/import.html', error="No file selected")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the file (implementation to be added later)
            # This would read the file, validate data, and create a project
            
            # Demo implementation (to be replaced with actual processing)
            try:
                # Read file data based on file type
                if filename.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:  # Excel file
                    df = pd.read_excel(file_path)
                
                # At this point, you'd parse the DataFrame and create a Project
                # For now, just redirect to the projects list page
                return redirect(url_for('list_projects'))
            
            except Exception as e:
                return render_template('projects/import.html', 
                                      error=f"Error processing file: {str(e)}")
        else:
            return render_template('projects/import.html', 
                                  error="Invalid file type. Please upload a CSV or Excel file.")
    
    return render_template('projects/import.html')

@app.route('/projects/<int:project_id>')
def view_project(project_id):
    """View a specific project"""
    project = Project.query.get_or_404(project_id)
    return render_template('projects/view.html', project=project)

@app.route('/analysis/<int:project_id>')
def analyze_project(project_id):
    """Financial analysis of a project"""
    project = Project.query.get_or_404(project_id)
    # This will be expanded with actual analysis logic
    return render_template('analysis/project.html', project=project)

@app.route('/api/calculate', methods=['POST'])
def calculate_metrics():
    """API endpoint for calculating financial metrics"""
    data = request.json
    # This will be implemented with actual calculation logic
    return jsonify({'status': 'success', 'metrics': {}})

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)