"""
Script to generate template files for the Energy Finance application.
"""

from utils import generate_project_templates

if __name__ == "__main__":
    print("Generating project templates...")
    templates = generate_project_templates()
    print(f"Templates created successfully:")
    print(f"Excel: {templates['excel_path']}")
    print(f"CSV: {templates['csv_path']}")