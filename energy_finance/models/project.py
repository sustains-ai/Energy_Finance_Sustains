"""
Project models for energy finance application.
"""

from datetime import datetime
from energy_finance.app import db


class Project(db.Model):
    """Base model for energy projects"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    capacity_mw = db.Column(db.Float, nullable=False)  # Capacity in MW
    project_type = db.Column(db.String(50), nullable=False)  # e.g., 'solar', 'wind'
    
    # Financial parameters
    capex = db.Column(db.Float)  # Capital expenditure (total)
    capex_per_mw = db.Column(db.Float)  # Capital expenditure per MW
    opex_per_year = db.Column(db.Float)  # Operating expenditure per year
    opex_per_mw = db.Column(db.Float)  # Operating expenditure per MW per year
    
    # Dates
    start_date = db.Column(db.Date)
    commercial_operation_date = db.Column(db.Date)
    expected_lifetime_years = db.Column(db.Integer, default=25)
    
    # Project status
    status = db.Column(db.String(50), default='planning')  # planning, construction, operational, decommissioned
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Discriminator for polymorphic identity
    type = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'project'
    }
    
    def __repr__(self):
        return f'<Project {self.name} ({self.capacity_mw} MW)>'


class SolarProject(Project):
    """Model for solar energy projects"""
    __tablename__ = 'solar_projects'
    
    id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    
    # Solar-specific parameters
    panel_type = db.Column(db.String(50))  # e.g., 'monocrystalline', 'polycrystalline', 'thin-film'
    panel_efficiency = db.Column(db.Float)  # efficiency percentage
    num_panels = db.Column(db.Integer)
    panel_capacity_w = db.Column(db.Float)  # capacity per panel in watts
    
    # Location parameters
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    tilt_angle = db.Column(db.Float)  # for fixed-tilt systems
    azimuth = db.Column(db.Float)  # orientation
    
    # Performance parameters
    degradation_rate = db.Column(db.Float, default=0.5)  # annual degradation rate (%)
    performance_ratio = db.Column(db.Float, default=0.75)  # ratio of actual to theoretical energy output
    
    # Land use
    land_area_acres = db.Column(db.Float)  # land area in acres
    
    # Tracking system (if any)
    tracking_type = db.Column(db.String(50), default='fixed')  # fixed, single-axis, dual-axis
    
    __mapper_args__ = {
        'polymorphic_identity': 'solar'
    }
    
    def __repr__(self):
        return f'<SolarProject {self.name} ({self.capacity_mw} MW)>'