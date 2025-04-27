"""
Utility functions for the Energy Finance application.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, date


def generate_project_templates():
    """
    Generate template Excel and CSV files for project data import.
    """
    # Create templates directory if it doesn't exist
    templates_dir = 'static/templates'
    os.makedirs(templates_dir, exist_ok=True)
    
    # Define the template structure with columns and example data
    template_data = {
        'name': ['Solar Farm Example', ''],
        'description': ['5.5 MW solar PV project located in California', ''],
        'location': ['Sunny Valley, CA', ''],
        'capacity_mw': [5.5, ''],
        'project_type': ['solar', ''],
        'capex': [5500000, ''],
        'capex_per_mw': [1000000, ''],
        'opex_per_year': [75000, ''],
        'opex_per_mw': [15000, ''],
        'start_date': [date(2025, 1, 1), ''],
        'commercial_operation_date': [date(2025, 6, 1), ''],
        'expected_lifetime_years': [25, ''],
        'status': ['planning', ''],
        'panel_type': ['monocrystalline', ''],
        'panel_efficiency': [21.5, ''],
        'num_panels': [13750, ''],
        'panel_capacity_w': [400, ''],
        'latitude': [34.5, ''],
        'longitude': [-118.2, ''],
        'tilt_angle': [20, ''],
        'azimuth': [180, ''],
        'degradation_rate': [0.5, ''],
        'performance_ratio': [0.75, ''],
        'land_area_acres': [25, ''],
        'tracking_type': ['fixed', '']
    }
    
    # Create dataframe
    df = pd.DataFrame(template_data)
    
    # Save as Excel template
    excel_path = os.path.join(templates_dir, 'solar_project_template.xlsx')
    
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Project Data', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Project Data']
        
        # Add a header format
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'bg_color': '#366092',
            'font_color': 'white',
            'border': 1
        })
        
        # Apply the header format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Add comments with descriptions
        descriptions = {
            'name': 'Name of the solar project',
            'description': 'Brief description of the project',
            'location': 'Physical location of the project',
            'capacity_mw': 'Capacity in megawatts (MW)',
            'project_type': 'Type of project (solar, wind, etc.)',
            'capex': 'Total capital expenditure ($)',
            'capex_per_mw': 'Capital expenditure per MW ($/MW)',
            'opex_per_year': 'Annual operating expenditure ($)',
            'opex_per_mw': 'Operating expenditure per MW ($/MW/year)',
            'start_date': 'Project start date (YYYY-MM-DD)',
            'commercial_operation_date': 'Commercial operation date (YYYY-MM-DD)',
            'expected_lifetime_years': 'Expected operational lifetime in years',
            'status': 'Current status (planning, construction, operational, decommissioned)',
            'panel_type': 'Solar panel type (monocrystalline, polycrystalline, thin-film, bifacial)',
            'panel_efficiency': 'Solar panel efficiency (%)',
            'num_panels': 'Number of solar panels',
            'panel_capacity_w': 'Capacity per panel (watts)',
            'latitude': 'Project latitude (decimal degrees)',
            'longitude': 'Project longitude (decimal degrees)',
            'tilt_angle': 'Panel tilt angle (degrees)',
            'azimuth': 'Panel azimuth angle (degrees, 180 = south)',
            'degradation_rate': 'Annual panel degradation rate (%)',
            'performance_ratio': 'System performance ratio (0-1)',
            'land_area_acres': 'Total land area (acres)',
            'tracking_type': 'Tracking system type (fixed, single-axis, dual-axis)'
        }
        
        for col_num, column in enumerate(df.columns):
            if column in descriptions:
                worksheet.write_comment(0, col_num, descriptions[column])
        
        # Set column widths
        worksheet.set_column(0, len(df.columns) - 1, 20)
        
        # Add a second sheet with instructions
        instructions_df = pd.DataFrame({
            'Field': list(descriptions.keys()),
            'Description': list(descriptions.values()),
            'Example': [template_data[col][0] for col in descriptions.keys()]
        })
        
        instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
        instructions_sheet = writer.sheets['Instructions']
        
        # Format the instructions sheet
        instructions_sheet.set_column(0, 0, 20)
        instructions_sheet.set_column(1, 1, 50)
        instructions_sheet.set_column(2, 2, 25)
    
    # Save as CSV template
    csv_path = os.path.join(templates_dir, 'solar_project_template.csv')
    df.to_csv(csv_path, index=False)
    
    return {
        'excel_path': excel_path,
        'csv_path': csv_path
    }


def calculate_financial_metrics(project, discount_rate=0.08, inflation_rate=0.025, debt_ratio=0.7, interest_rate=0.05):
    """
    Calculate financial metrics for a project.
    
    Parameters:
    - project: A Project instance
    - discount_rate: Discount rate (default 8%)
    - inflation_rate: Inflation rate (default 2.5%)
    - debt_ratio: Debt to capital ratio (default 70%)
    - interest_rate: Interest rate on debt (default 5%)
    
    Returns: FinancialMetric instance
    """
    # This is a placeholder implementation
    # In a real application, this would perform actual financial calculations
    
    # Example calculation for NPV
    npv = 0
    irr = 0
    payback_period = 0
    lcoe = 0
    
    # In a real implementation, we would:
    # 1. Generate cash flows for each year of the project
    # 2. Calculate NPV using the discount rate
    # 3. Calculate IRR by solving for the discount rate that makes NPV = 0
    # 4. Calculate payback period by finding when cumulative cash flow becomes positive
    # 5. Calculate LCOE by dividing total costs by total energy production
    
    # Return financial metrics
    return {
        'npv': npv,
        'irr': irr,
        'payback_period': payback_period,
        'lcoe': lcoe,
        'discount_rate': discount_rate,
        'inflation_rate': inflation_rate,
        'debt_ratio': debt_ratio,
        'interest_rate': interest_rate
    }


def estimate_energy_production(solar_project, year):
    """
    Estimate energy production for a solar project in a given year.
    
    Parameters:
    - solar_project: A SolarProject instance
    - year: Year of operation (0-based, where 0 is the first year)
    
    Returns: Estimated energy production in MWh
    """
    # This is a placeholder implementation
    # In a real application, this would use location, panel characteristics, etc.
    
    # Basic calculation:
    # 1. Calculate theoretical production based on capacity
    # 2. Apply performance ratio
    # 3. Apply degradation over time
    
    if not solar_project.capacity_mw:
        return 0
    
    # Typical capacity factor for solar PV (location dependent)
    capacity_factor = 0.2  # 20%
    
    # Hours in a year
    hours_per_year = 8760
    
    # Base production in MWh
    base_production = solar_project.capacity_mw * capacity_factor * hours_per_year
    
    # Apply performance ratio
    if solar_project.performance_ratio:
        base_production *= solar_project.performance_ratio
    
    # Apply degradation over time
    if solar_project.degradation_rate and year > 0:
        degradation_factor = (1 - solar_project.degradation_rate / 100) ** year
        base_production *= degradation_factor
    
    return base_production