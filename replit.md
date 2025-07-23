# KPI Reporting Dashboard

## Overview

This is a Streamlit-based KPI (Key Performance Indicator) reporting dashboard that allows users to upload Excel files containing KPI data and generate interactive reports and comparisons. The application provides data visualization capabilities with charts and tables, enabling users to analyze KPI performance across different time periods.

## User Preferences

Preferred communication style: Simple, everyday language.

### Dashboard Structure Requirements (Updated):
- Reports section: User selects time period type (monthly/quarterly/half-yearly/annually), specific period, and year
- Display KPIs grouped by department (departments as rows, KPIs as columns)
- Comparisons section: Same structure but allows comparing different periods
- Excel file must include: kpi_id, kpi_name, department, month, quarter, year, value, data_type
- Smart calculation logic: percentages averaged, numbers summed for aggregated periods

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid development of data applications with minimal frontend code
- **Layout**: Wide layout with expandable sidebar for optimal dashboard viewing experience
- **Components**: Modular component structure separating reports and comparisons functionality
- **State Management**: Streamlit session state for maintaining data and processor instances across interactions

### Backend Architecture
- **Data Processing**: Custom DataProcessor class handles Excel file parsing, data validation, and aggregation
- **Visualization**: ChartGenerator utility class creates interactive Plotly charts
- **File Handling**: Direct Excel file upload processing without persistent storage
- **Session Management**: In-memory data storage using Streamlit's session state

## Key Components

### Main Application (`app.py`)
- Entry point that configures Streamlit page settings
- Handles file upload and data validation
- Manages navigation between reports and comparisons sections
- Validates required Excel columns: kpi_id, kpi_name, month, quarter, year, value

### Data Processing (`utils/data_processor.py`)
- **DataProcessor Class**: Core data handling component
- **Functionality**: Data cleaning, type conversion, time period aggregation
- **Validation**: Ensures data integrity with range checks for months (1-12) and quarters (1-4)
- **Time Periods**: Supports monthly, quarterly, half-yearly, and annual aggregations

### Chart Generation (`utils/chart_generator.py`)
- **ChartGenerator Class**: Creates interactive visualizations using Plotly
- **Chart Types**: Line charts for trends, bar charts for comparisons
- **Features**: Interactive hover, customizable titles, responsive design

### UI Components
- **Reports Component** (`components/reports.py`): Displays detailed KPI reports with filtering
- **Comparisons Component** (`components/comparisons.py`): Shows period-over-period analysis

## Data Flow

1. **Upload**: User uploads Excel file through Streamlit file uploader
2. **Validation**: System checks for required columns and data format
3. **Processing**: DataProcessor cleans and transforms raw data
4. **Storage**: Processed data stored in session state
5. **Filtering**: Users apply filters for KPIs, years, and time periods
6. **Visualization**: ChartGenerator creates interactive charts based on filtered data
7. **Display**: Results shown in reports or comparisons sections

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for data apps
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **NumPy**: Numerical computing support

### File Processing
- **Excel Support**: Built-in pandas Excel reading capabilities (.xlsx, .xls formats)
- **No Database**: Application operates entirely in-memory without persistent storage

## Deployment Strategy

### Local Development
- Standard Python environment with pip requirements
- Streamlit's built-in development server (`streamlit run app.py`)

### Production Considerations
- **Stateless Design**: No persistent data storage, suitable for container deployment
- **Session Management**: Uses Streamlit's session state for user data persistence
- **File Upload Limits**: Dependent on Streamlit's default file size limitations
- **Memory Management**: Data stored temporarily in application memory during user session

### Scalability Limitations
- Single-user session design
- In-memory data processing limits large file handling
- No concurrent user data isolation beyond Streamlit's session management

The architecture prioritizes simplicity and rapid development over scalability, making it ideal for individual use or small team KPI analysis workflows.