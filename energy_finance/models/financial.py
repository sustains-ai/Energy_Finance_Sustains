"""
Financial models for energy finance application.
"""

from datetime import datetime
from energy_finance.app import db


class CashFlow(db.Model):
    """Model for tracking project cash flows"""
    __tablename__ = 'cash_flows'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    # Time period
    year = db.Column(db.Integer, nullable=False)  # 0 for initial investment, 1-N for operational years
    
    # Cash flow components
    capex = db.Column(db.Float, default=0.0)  # Capital expenditures (negative)
    revenue = db.Column(db.Float, default=0.0)  # Revenue from electricity sales
    opex = db.Column(db.Float, default=0.0)  # Operating expenses (negative)
    maintenance = db.Column(db.Float, default=0.0)  # Maintenance costs (negative)
    insurance = db.Column(db.Float, default=0.0)  # Insurance costs (negative)
    taxes = db.Column(db.Float, default=0.0)  # Taxes (negative)
    debt_service = db.Column(db.Float, default=0.0)  # Debt payments (negative)
    incentives = db.Column(db.Float, default=0.0)  # Tax credits, grants, etc. (positive)
    salvage_value = db.Column(db.Float, default=0.0)  # End-of-life value
    
    # Energy production for the period
    energy_production_mwh = db.Column(db.Float, default=0.0)  # Energy produced in MWh
    
    # Calculated totals
    net_cash_flow = db.Column(db.Float, default=0.0)  # Net cash flow for the period
    cumulative_cash_flow = db.Column(db.Float, default=0.0)  # Running total of cash flows
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref=db.backref('cash_flows', lazy=True))
    
    def __repr__(self):
        return f'<CashFlow Project={self.project_id} Year={self.year} Net={self.net_cash_flow}>'


class FinancialMetric(db.Model):
    """Model for storing calculated financial metrics for a project"""
    __tablename__ = 'financial_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, unique=True)
    
    # Core financial metrics
    npv = db.Column(db.Float)  # Net Present Value
    irr = db.Column(db.Float)  # Internal Rate of Return (%)
    payback_period = db.Column(db.Float)  # Payback period in years
    lcoe = db.Column(db.Float)  # Levelized Cost of Energy ($/MWh)
    
    # Additional metrics
    mirr = db.Column(db.Float)  # Modified Internal Rate of Return (%)
    profitability_index = db.Column(db.Float)  # Profitability Index
    debt_service_coverage_ratio = db.Column(db.Float)  # DSCR
    
    # Key inputs used to calculate metrics
    discount_rate = db.Column(db.Float)  # Discount rate used (%)
    inflation_rate = db.Column(db.Float)  # Inflation rate used (%)
    debt_ratio = db.Column(db.Float)  # Debt to total capital ratio
    interest_rate = db.Column(db.Float)  # Interest rate on debt (%)
    
    # PPA details if applicable
    ppa_price = db.Column(db.Float)  # Power Purchase Agreement price ($/MWh)
    ppa_escalation = db.Column(db.Float)  # Annual escalation rate for PPA (%)
    ppa_term = db.Column(db.Integer)  # PPA term in years
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref=db.backref('financial_metrics', uselist=False))
    
    def __repr__(self):
        return f'<FinancialMetric Project={self.project_id} NPV={self.npv} IRR={self.irr}>'