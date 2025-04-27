# Energy Finance

A powerful tool for financial analysis of energy projects with a focus on solar power.

Developed by [Sustains.ai](https://sustains.ai) - Building sustainable technology solutions for businesses.

## Overview

Energy Finance is a Flask-based web application designed to help energy analysts evaluate the financial viability of renewable energy projects. The platform provides capabilities for calculating key financial metrics like IRR, NPV, and LCOE, as well as generating detailed cash flow projections.

## Features

- **Project Management**: Create, view, and analyze energy projects
- **Financial Analysis**: Calculate key financial metrics including NPV, IRR, Payback Period, and LCOE
- **Solar-Specific Modeling**: Detailed modeling for solar energy projects
- **Dual Input Options**: Input data through a user-friendly form or import from Excel/CSV
- **Template Downloads**: Generate formatted templates for data import

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sustains-ai/Energy_Finance_Sustains.git
cd Energy_Finance_Sustains
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
python main.py
```

## Usage

1. Access the application at http://localhost:5000
2. Create a new project using the form or import from Excel/CSV
3. View project details and financial metrics
4. Analyze cash flows and financial performance

## Development

- **Models**: The application uses SQLAlchemy models for project data storage
- **Templates**: Jinja2 templates for the UI
- **Bootstrap**: Uses Bootstrap for responsive design

## License

This project is licensed under the MIT License - see the LICENSE file for details.