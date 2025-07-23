#!/usr/bin/env python3
"""
Create a sample KPI Excel file for testing the dashboard
"""
import pandas as pd
import numpy as np
from datetime import datetime

def create_sample_kpi_data():
    """Create sample KPI data for demonstration"""
    
    # Define KPIs with departments and data types
    kpis = [
        {"id": 1, "name": "Revenue", "department": "Sales", "data_type": "number"},
        {"id": 2, "name": "Customer Satisfaction", "department": "Customer Service", "data_type": "percentage"},
        {"id": 3, "name": "Sales Volume", "department": "Sales", "data_type": "number"},
        {"id": 4, "name": "Website Traffic", "department": "Marketing", "data_type": "number"},
        {"id": 5, "name": "Conversion Rate", "department": "Marketing", "data_type": "percentage"},
        {"id": 6, "name": "Employee Satisfaction", "department": "HR", "data_type": "percentage"},
        {"id": 7, "name": "Production Efficiency", "department": "Operations", "data_type": "percentage"},
        {"id": 8, "name": "Cost per Acquisition", "department": "Marketing", "data_type": "number"}
    ]
    
    # Generate data for 2022-2024
    years = [2022, 2023, 2024]
    months = list(range(1, 13))
    
    data = []
    
    # Generate realistic sample data
    np.random.seed(42)  # For consistent results
    
    for year in years:
        for month in months:
            quarter = ((month - 1) // 3) + 1
            
            for kpi in kpis:
                # Create different patterns for different KPIs
                if kpi["name"] == "Revenue":
                    # Revenue grows over time with seasonal patterns
                    base_value = 50000 + (year - 2022) * 10000
                    seasonal_factor = 1.2 if month in [11, 12] else 1.0  # Holiday boost
                    monthly_variation = np.random.normal(1.0, 0.1)
                    value = base_value * seasonal_factor * monthly_variation
                    
                elif kpi["name"] == "Customer Satisfaction":
                    # Customer satisfaction as percentage (70-95%)
                    base_value = 80 + (year - 2022) * 2
                    value = base_value + np.random.normal(0, 3)
                    value = max(70, min(95, value))  # Keep within reasonable bounds
                    
                elif kpi["name"] == "Sales Volume":
                    # Sales volume in units
                    base_value = 1000 + (year - 2022) * 200
                    seasonal_factor = 1.3 if month in [11, 12] else 1.0
                    value = base_value * seasonal_factor * np.random.normal(1.0, 0.15)
                    
                elif kpi["name"] == "Website Traffic":
                    # Website visitors
                    base_value = 25000 + (year - 2022) * 5000
                    value = base_value * np.random.normal(1.0, 0.2)
                    
                elif kpi["name"] == "Conversion Rate":
                    # Conversion rate as percentage (2-8%)
                    base_value = 4 + (year - 2022) * 0.5
                    value = base_value + np.random.normal(0, 0.5)
                    value = max(2, min(8, value))
                
                elif kpi["name"] == "Employee Satisfaction":
                    # Employee satisfaction as percentage (60-90%)
                    base_value = 75 + (year - 2022) * 1
                    value = base_value + np.random.normal(0, 2)
                    value = max(60, min(90, value))
                
                elif kpi["name"] == "Production Efficiency":
                    # Production efficiency as percentage (70-95%)
                    base_value = 80 + (year - 2022) * 2
                    value = base_value + np.random.normal(0, 3)
                    value = max(70, min(95, value))
                
                elif kpi["name"] == "Cost per Acquisition":
                    # Cost per acquisition in dollars (decreasing is better)
                    base_value = 50 - (year - 2022) * 5  # Improving over time
                    value = base_value * np.random.normal(1.0, 0.1)
                    value = max(20, value)  # Keep above minimum
                
                data.append({
                    "kpi_id": kpi["id"],
                    "kpi_name": kpi["name"],
                    "department": kpi["department"],
                    "month": month,
                    "quarter": quarter,
                    "year": year,
                    "value": round(value, 2),
                    "data_type": kpi["data_type"]
                })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to Excel file
    df.to_excel("sample_kpi_data.xlsx", index=False)
    print(f"Created sample_kpi_data.xlsx with {len(df)} records")
    print("\nSample data preview:")
    print(df.head(10))
    print(f"\nData covers years: {df['year'].min()} - {df['year'].max()}")
    print(f"KPIs included: {', '.join(df['kpi_name'].unique())}")
    
    return df

if __name__ == "__main__":
    create_sample_kpi_data()