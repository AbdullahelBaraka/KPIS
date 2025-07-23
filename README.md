# KPI Reporting Dashboard

A powerful Streamlit-based KPI reporting platform that transforms Excel data into interactive, visually compelling reports with advanced data visualization and export capabilities.

## Features

- **Interactive Reports**: Generate detailed KPI reports with department grouping
- **Period Comparisons**: Compare KPIs across different time periods (monthly/quarterly/half-yearly/annually)
- **Smart Calculations**: Automatic aggregation logic - percentages averaged, numbers summed
- **Interactive Charts**: Individual charts for each KPI comparison
- **Professional PDFs**: Export reports and comparisons as high-quality PDF documents
- **Excel Integration**: Simple Excel file upload with structured data format

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/kpi-dashboard.git
cd kpi-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Excel Data Format

Your Excel file must include the following columns:
- `kpi_id`: Unique identifier for each KPI
- `kpi_name`: Display name of the KPI
- `department`: Department name
- `month`: Month (1-12)
- `quarter`: Quarter (1-4)
- `year`: Year
- `value`: KPI value
- `data_type`: Either "percentage" or "number" (determines calculation method)

## Usage

1. **Upload Data**: Upload your Excel file with KPI data
2. **Reports Tab**: 
   - Select time period type (monthly/quarterly/half-yearly/annually)
   - Choose specific period and year
   - View department-grouped KPI reports
   - Download PDF reports
3. **Comparison Tab**:
   - Select comparison type
   - Choose two different periods
   - View individual KPI comparison charts
   - Download comparison reports

## Sample Data

Use `sample_kpi_data.xlsx` to test the application with sample data, or run `sample_kpi_data.py` to generate new sample data.

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **ReportLab**: PDF report generation
- **NumPy**: Numerical computing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).