import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
import plotly.express as px
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def create_pdf_report(filtered_data, period_name, value_type):
    """Generate a high-quality PDF report with proper page breaks"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=50)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle', 
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#00D4AA'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'], 
        fontSize=14,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666')
    )
    
    dept_style = ParagraphStyle(
        'DeptHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=8,
        spaceBefore=15,
        textColor=colors.HexColor('#00D4AA'),
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        backColor=colors.HexColor('#E6FFFA'),
        borderWidth=2,
        borderColor=colors.HexColor('#00D4AA'),
        borderPadding=10,
        borderRadius=5
    )
    
    # Add title and header
    title = Paragraph("KPI Dashboard Report", title_style)
    elements.append(title)
    
    # Add subtitle with period info
    subtitle_text = f"{period_name}<br/><font color='#888888' size='11'>{value_type} | Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</font>"
    subtitle = Paragraph(subtitle_text, subtitle_style)
    elements.append(subtitle)
    
    # Group by department
    departments = filtered_data['department'].unique()
    
    for i, dept in enumerate(sorted(departments)):
        dept_data = filtered_data[filtered_data['department'] == dept]
        
        # Create department section elements
        dept_elements = []
        
        # Department header
        dept_header = Paragraph(f"{dept} Department", dept_style)
        dept_elements.append(dept_header)
        dept_elements.append(Spacer(1, 10))
        
        # Create table data for this department
        table_data = [['KPI Name', 'Value']]  # Header row
        
        for _, row in dept_data.iterrows():
            table_data.append([row['kpi_name'], f"{row['value']:.2f}"])
        
        # Create table with improved styling
        table = Table(table_data, colWidths=[4*inch, 1.5*inch], repeatRows=1)
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D4AA')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),  # Right align values
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DDDDDD')),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            
            # Padding
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            
            # Header specific styling
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        
        dept_elements.append(table)
        
        # Keep department header and table together
        dept_section = KeepTogether(dept_elements)
        elements.append(dept_section)
        
        # Add space between departments (but not after the last one)
        if i < len(departments) - 1:
            elements.append(Spacer(1, 25))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_comparison_pdf(comparison_data, period_1_name, period_2_name):
    """Generate a high-quality PDF comparison report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=50)
    
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle', 
        parent=styles['Heading1'],
        fontSize=22,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#00D4AA'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'], 
        fontSize=14,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#666666')
    )
    
    dept_style = ParagraphStyle(
        'DeptHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=8,
        spaceBefore=15,
        textColor=colors.HexColor('#00D4AA'),
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        backColor=colors.HexColor('#E6FFFA'),
        borderWidth=2,
        borderColor=colors.HexColor('#00D4AA'),
        borderPadding=10
    )
    
    # Add title and header
    title = Paragraph("KPI Comparison Report", title_style)
    elements.append(title)
    
    subtitle_text = f"{period_1_name} vs {period_2_name}<br/><font color='#888888' size='11'>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</font>"
    subtitle = Paragraph(subtitle_text, subtitle_style)
    elements.append(subtitle)
    
    # Group by department
    departments = comparison_data['department'].unique()
    
    for i, dept in enumerate(sorted(departments)):
        dept_data = comparison_data[comparison_data['department'] == dept]
        
        # Create department section elements
        dept_elements = []
        
        # Department header
        dept_header = Paragraph(f"{dept} Department", dept_style)
        dept_elements.append(dept_header)
        dept_elements.append(Spacer(1, 10))
        
        # Create comparison table
        table_data = [['KPI Name', period_1_name, period_2_name, 'Change %']]
        
        for _, row in dept_data.iterrows():
            change_pct = row['change_percent']
            change_text = f"{change_pct:+.1f}%" if pd.notna(change_pct) else "N/A"
            table_data.append([
                row['kpi_name'], 
                f"{row['period_1_value']:.2f}",
                f"{row['period_2_value']:.2f}", 
                change_text
            ])
        
        # Create table with improved styling
        table = Table(table_data, colWidths=[2.2*inch, 1.2*inch, 1.2*inch, 1*inch], repeatRows=1)
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00D4AA')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),  # Right align values
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            
            # Data rows styling
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#DDDDDD')),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
            
            # Padding
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        dept_elements.append(table)
        
        # Keep department section together
        dept_section = KeepTogether(dept_elements)
        elements.append(dept_section)
        
        # Add space between departments
        if i < len(departments) - 1:
            elements.append(Spacer(1, 25))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def comparison_function(df):
    """Comparison function that compares KPIs between two different periods"""
    
    st.header("📊 Period Comparison")
    
    # Comparison type selection
    comparison_type = st.selectbox(
        "Comparison Type",
        ["monthly", "quarterly", "half_annual", "annually"],
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    # Create two columns for period selection
    col1, col2 = st.columns(2)
    
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                   5: 'May', 6: 'June', 7: 'July', 8: 'August', 
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    
    with col1:
        st.subheader("📅 First Period")
        years = sorted(df['year'].unique())
        selected_year_1 = st.selectbox("Year", years, key="year1")
        
        if comparison_type == "monthly":
            available_months = sorted(df[df['year'] == selected_year_1]['month'].unique())
            selected_period_1 = st.selectbox(
                "Month", 
                available_months,
                format_func=lambda x: month_names[x],
                key="month1"
            )
        elif comparison_type == "quarterly":
            available_quarters = sorted(df[df['year'] == selected_year_1]['quarter'].unique())
            selected_period_1 = st.selectbox("Quarter", available_quarters, key="quarter1")
        elif comparison_type == "half_annual":
            selected_period_1 = st.selectbox(
                "Half", 
                [1, 2], 
                format_func=lambda x: "First Half" if x == 1 else "Second Half",
                key="half1"
            )
        else:  # annually
            selected_period_1 = None
    
    with col2:
        st.subheader("📅 Second Period")
        selected_year_2 = st.selectbox("Year", years, key="year2")
        
        if comparison_type == "monthly":
            available_months = sorted(df[df['year'] == selected_year_2]['month'].unique())
            selected_period_2 = st.selectbox(
                "Month", 
                available_months,
                format_func=lambda x: month_names[x],
                key="month2"
            )
        elif comparison_type == "quarterly":
            available_quarters = sorted(df[df['year'] == selected_year_2]['quarter'].unique())
            selected_period_2 = st.selectbox("Quarter", available_quarters, key="quarter2")
        elif comparison_type == "half_annual":
            selected_period_2 = st.selectbox(
                "Half", 
                [1, 2], 
                format_func=lambda x: "First Half" if x == 1 else "Second Half",
                key="half2"
            )
        else:  # annually
            selected_period_2 = None
    
    # Compare button
    if st.button("Compare Periods", type="primary"):
        # Helper function to get period data using same logic as report function
        def get_period_data(comparison_type, selected_year, selected_period):
            if comparison_type == "monthly":
                filtered_data = df[(df['year'] == selected_year) & (df['month'] == selected_period)]
                period_name = f"{month_names[selected_period]} {selected_year}"
                
            elif comparison_type == "quarterly":
                filtered_data = df[(df['year'] == selected_year) & (df['quarter'] == selected_period)]
                
                # Group and calculate based on data type
                result_data = []
                for (dept, kpi), group in filtered_data.groupby(['department', 'kpi_name']):
                    data_type = group['data_type'].iloc[0]
                    if data_type == "percentage":
                        value = group['value'].mean()
                    else:
                        value = group['value'].sum()
                    result_data.append({'department': dept, 'kpi_name': kpi, 'value': value, 'data_type': data_type})
                
                filtered_data = pd.DataFrame(result_data)
                period_name = f"Q{selected_period} {selected_year}"
                
            elif comparison_type == "half_annual":
                if selected_period == 1:
                    filtered_data = df[(df['year'] == selected_year) & (df['month'].isin([1,2,3,4,5,6]))]
                else:
                    filtered_data = df[(df['year'] == selected_year) & (df['month'].isin([7,8,9,10,11,12]))]
                
                # Group and calculate based on data type
                result_data = []
                for (dept, kpi), group in filtered_data.groupby(['department', 'kpi_name']):
                    data_type = group['data_type'].iloc[0]
                    if data_type == "percentage":
                        value = group['value'].mean()
                    else:
                        value = group['value'].sum()
                    result_data.append({'department': dept, 'kpi_name': kpi, 'value': value, 'data_type': data_type})
                
                filtered_data = pd.DataFrame(result_data)
                period_name = f"{'First' if selected_period == 1 else 'Second'} Half {selected_year}"
                
            else:  # annually
                filtered_data = df[df['year'] == selected_year]
                
                # Group and calculate based on data type
                result_data = []
                for (dept, kpi), group in filtered_data.groupby(['department', 'kpi_name']):
                    data_type = group['data_type'].iloc[0]
                    if data_type == "percentage":
                        value = group['value'].mean()
                    else:
                        value = group['value'].sum()
                    result_data.append({'department': dept, 'kpi_name': kpi, 'value': value, 'data_type': data_type})
                
                filtered_data = pd.DataFrame(result_data)
                period_name = f"Year {selected_year}"
            
            return filtered_data, period_name
        
        # Get data for both periods
        data_1, period_1_name = get_period_data(comparison_type, selected_year_1, selected_period_1)
        data_2, period_2_name = get_period_data(comparison_type, selected_year_2, selected_period_2)
        
        if data_1.empty or data_2.empty:
            st.warning("No data found for one or both selected periods")
            return
        
        # Merge data for comparison
        comparison_data = data_1.merge(
            data_2, 
            on=['department', 'kpi_name'], 
            suffixes=('_1', '_2'),
            how='inner'
        )
        
        if comparison_data.empty:
            st.warning("No common KPIs found between the selected periods")
            return
        
        # Rename columns for clarity
        comparison_data = comparison_data.rename(columns={
            'value_1': 'period_1_value',
            'value_2': 'period_2_value'
        })
        
        # Calculate percentage change
        comparison_data['change_percent'] = ((comparison_data['period_2_value'] - comparison_data['period_1_value']) / 
                                           comparison_data['period_1_value'].abs()) * 100
        
        # Display results
        st.success("✅ Comparison Generated Successfully!")
        st.subheader(f"📊 Comparing: {period_1_name} vs {period_2_name}")
        
        # Group by department and display
        departments = comparison_data['department'].unique()
        
        for dept in sorted(departments):
            dept_data = comparison_data[comparison_data['department'] == dept]
            
            # Modern department header
            st.markdown(f'<div class="dept-header">🏢 {dept} Department</div>', unsafe_allow_html=True)
            
            # Create individual charts for each KPI in this department
            for _, kpi_row in dept_data.iterrows():
                kpi_name = kpi_row['kpi_name']
                period_1_value = kpi_row['period_1_value']
                period_2_value = kpi_row['period_2_value']
                
                # Create individual KPI chart
                fig = go.Figure()
                
                # Add bar chart for comparison
                fig.add_trace(go.Bar(
                    x=[period_1_name, period_2_name],
                    y=[period_1_value, period_2_value],
                    marker_color=['#00D4AA', '#9C27B0'],
                    text=[f'{period_1_value:.2f}', f'{period_2_value:.2f}'],
                    textposition='auto',
                    name=kpi_name
                ))
                
                # Calculate change for title
                change_pct = kpi_row['change_percent']
                change_text = f" ({change_pct:+.1f}%)" if pd.notna(change_pct) else ""
                
                # Update layout
                fig.update_layout(
                    title=f"{kpi_name}{change_text}",
                    xaxis_title="Periods",
                    yaxis_title="Value",
                    height=300,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)'),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Display comparison table
            st.subheader(f"📋 {dept} Department - Detailed Comparison")
            
            # Prepare table data
            table_data = []
            for _, row in dept_data.iterrows():
                change_pct = row['change_percent']
                change_display = f"{change_pct:+.1f}%" if pd.notna(change_pct) else "N/A"
                
                table_data.append({
                    'KPI Name': row['kpi_name'],
                    period_1_name: f"{row['period_1_value']:.2f}",
                    period_2_name: f"{row['period_2_value']:.2f}",
                    'Change %': change_display
                })
            
            # Display table
            table_df = pd.DataFrame(table_data)
            st.dataframe(table_df, use_container_width=True, hide_index=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Add download section
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate PDF
            pdf_buffer = create_comparison_pdf(comparison_data, period_1_name, period_2_name)
            st.download_button(
                label="📄 Download PDF Comparison",
                data=pdf_buffer,
                file_name=f"KPI_Comparison_{period_1_name.replace(' ', '_')}_vs_{period_2_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                type="secondary"
            )
        
        with col2:
            # Generate CSV
            csv_data = comparison_data[['department', 'kpi_name', 'period_1_value', 'period_2_value', 'change_percent']].to_csv(index=False)
            st.download_button(
                label="📊 Download CSV Data",
                data=csv_data,
                file_name=f"KPI_Comparison_{period_1_name.replace(' ', '_')}_vs_{period_2_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                type="secondary"
            )

def report_function(df):
    """Report function that displays KPIs grouped by department"""
    
    st.header("📊 Reports")
    
    # Time period selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        period_type = st.selectbox(
            "Report Type",
            ["monthly", "quarterly", "half_annual", "annually"]
        )
    
    with col2:
        # Get available years from data
        years = sorted(df['year'].unique())
        selected_year = st.selectbox("Year", years)
    
    with col3:
        if period_type == "monthly":
            # Get available months for selected year
            available_months = sorted(df[df['year'] == selected_year]['month'].unique())
            month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                          5: 'May', 6: 'June', 7: 'July', 8: 'August', 
                          9: 'September', 10: 'October', 11: 'November', 12: 'December'}
            selected_period = st.selectbox(
                "Month", 
                available_months,
                format_func=lambda x: month_names[x]
            )
        elif period_type == "quarterly":
            available_quarters = sorted(df[df['year'] == selected_year]['quarter'].unique())
            selected_period = st.selectbox("Quarter", available_quarters)
        elif period_type == "half_annual":
            selected_period = st.selectbox(
                "Half", 
                [1, 2], 
                format_func=lambda x: "First Half" if x == 1 else "Second Half"
            )
        else:  # annually
            selected_period = None
    
    # Show Report button
    if st.button("Show Report", type="primary"):
        # Filter and calculate data based on selection
        if period_type == "monthly":
            # Get exact values for the specific month
            filtered_data = df[(df['year'] == selected_year) & (df['month'] == selected_period)]
            period_name = f"{month_names[selected_period]} {selected_year}"
            value_type = "Exact values"
            
        elif period_type == "quarterly":
            # Filter data for the quarter
            filtered_data = df[(df['year'] == selected_year) & (df['quarter'] == selected_period)]
            
            # Group and calculate based on data type
            result_data = []
            for (dept, kpi), group in filtered_data.groupby(['department', 'kpi_name']):
                data_type = group['data_type'].iloc[0]  # Assume same data_type for same KPI
                if data_type == "percentage":
                    value = group['value'].mean()  # Average for percentages
                else:
                    value = group['value'].sum()   # Sum for numbers
                result_data.append({'department': dept, 'kpi_name': kpi, 'value': value, 'data_type': data_type})
            
            filtered_data = pd.DataFrame(result_data)
            period_name = f"Q{selected_period} {selected_year}"
            value_type = "Calculated values (avg for %, sum for numbers)"
            
        elif period_type == "half_annual":
            # Filter data for the half year
            if selected_period == 1:
                # First half: months 1-6
                filtered_data = df[(df['year'] == selected_year) & (df['month'].isin([1,2,3,4,5,6]))]
            else:
                # Second half: months 7-12
                filtered_data = df[(df['year'] == selected_year) & (df['month'].isin([7,8,9,10,11,12]))]
            
            # Group and calculate based on data type
            result_data = []
            for (dept, kpi), group in filtered_data.groupby(['department', 'kpi_name']):
                data_type = group['data_type'].iloc[0]  # Assume same data_type for same KPI
                if data_type == "percentage":
                    value = group['value'].mean()  # Average for percentages
                else:
                    value = group['value'].sum()   # Sum for numbers
                result_data.append({'department': dept, 'kpi_name': kpi, 'value': value, 'data_type': data_type})
            
            filtered_data = pd.DataFrame(result_data)
            period_name = f"{'First' if selected_period == 1 else 'Second'} Half {selected_year}"
            value_type = "Calculated values (avg for %, sum for numbers)"
            
        else:  # annually
            # Filter data for the entire year
            filtered_data = df[df['year'] == selected_year]
            
            # Group and calculate based on data type
            result_data = []
            for (dept, kpi), group in filtered_data.groupby(['department', 'kpi_name']):
                data_type = group['data_type'].iloc[0]  # Assume same data_type for same KPI
                if data_type == "percentage":
                    value = group['value'].mean()  # Average for percentages
                else:
                    value = group['value'].sum()   # Sum for numbers
                result_data.append({'department': dept, 'kpi_name': kpi, 'value': value, 'data_type': data_type})
            
            filtered_data = pd.DataFrame(result_data)
            period_name = f"Year {selected_year}"
            value_type = "Calculated values (avg for %, sum for numbers)"
        
        # Check if data exists
        if filtered_data.empty:
            st.warning("No data found for the selected period")
            return
        
        # Display report
        st.success("✅ Report Generated Successfully!")
        st.subheader(f"📈 KPI Report - {period_name}")
        st.caption(f"Showing {value_type}")
        
        # Add custom CSS for modern styling
        st.markdown("""
        <style>
        .kpi-card {
            background: linear-gradient(135deg, #00D4AA 0%, #4AE54A 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 212, 170, 0.2);
        }
        .kpi-name {
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 0.3rem;
        }
        .kpi-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        .dept-header {
            background: linear-gradient(90deg, #00D4AA 0%, #2DD4BF 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0 0.5rem 0;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Group by department and display
        departments = filtered_data['department'].unique()
        
        for dept in sorted(departments):
            dept_data = filtered_data[filtered_data['department'] == dept]
            
            # Modern department header
            st.markdown(f'<div class="dept-header">🏢 {dept} Department</div>', unsafe_allow_html=True)
            
            # Display KPIs in a grid layout
            kpi_list = dept_data.to_dict('records')
            
            # Create columns for KPI cards (2 per row)
            for i in range(0, len(kpi_list), 2):
                cols = st.columns(2)
                
                for j, col in enumerate(cols):
                    if i + j < len(kpi_list):
                        kpi = kpi_list[i + j]
                        with col:
                            st.markdown(f"""
                            <div class="kpi-card">
                                <div class="kpi-name">📊 {kpi['kpi_name']}</div>
                                <div class="kpi-value">{kpi['value']:.2f}</div>
                            </div>
                            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Add download section
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate PDF
            pdf_buffer = create_pdf_report(filtered_data, period_name, value_type)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"KPI_Report_{period_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                type="secondary"
            )
        
        with col2:
            # Generate CSV
            csv_data = filtered_data.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV Data",
                data=csv_data,
                file_name=f"KPI_Data_{period_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                type="secondary"
            )

# Main app
st.set_page_config(page_title="KPI Dashboard", layout="wide")

# Global minimal modern styling
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Modern font and spacing */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #ffffff;
        min-height: 100vh;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background: #ffffff;
    }
    
    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00D4AA 0%, #4AE54A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }
    
    /* Content sections */
    .content-section {
        background: #ffffff;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        border: none;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00D4AA 0%, #4AE54A 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 170, 0.4);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #00D4AA;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1);
    }
    
    /* Success/Info message styling */
    .stSuccess {
        background: linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%);
        border: 1px solid #4AE54A;
        border-radius: 8px;
        padding: 1rem;
        color: #15803D;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #E6FFFA 0%, #B2F5EA 100%);
        border: 1px solid #00D4AA;
        border-radius: 8px;
        padding: 1rem;
        color: #0D9488;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: white;
        border: 2px dashed #dee2e6;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #00D4AA;
        background: #f0fffe;
    }
</style>
""", unsafe_allow_html=True)

# Modern title
st.markdown('<h1 class="main-title">📊 KPI Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your data and generate beautiful reports grouped by department</p>', unsafe_allow_html=True)

# File upload in sidebar
with st.sidebar:
    st.markdown("### 📁 Upload Data")
    uploaded_file = st.file_uploader(
        "Choose Excel file",
        type=['xlsx', 'xls'],
        help="File should contain: kpi_id, kpi_name, department, month, quarter, year, value, data_type"
    )

# Main content
if uploaded_file is None:
    st.info("Please upload an Excel file to get started")
    st.markdown("""
    **Required Excel columns:**
    - kpi_id
    - kpi_name  
    - department
    - month (1-12)
    - quarter (1-4)
    - year
    - value
    - data_type ("percentage" or "number")
    """)
else:
    try:
        # Load and validate data
        df = pd.read_excel(uploaded_file)
        required_cols = ['kpi_id', 'kpi_name', 'department', 'month', 'quarter', 'year', 'value', 'data_type']
        
        if not all(col in df.columns for col in required_cols):
            st.error(f"Missing required columns. Found: {list(df.columns)}")
        else:
            st.success(f"Data loaded successfully! {len(df)} records found")
            
            # Navigation tabs
            tab1, tab2 = st.tabs(["📊 Reports", "📈 Comparison"])
            
            with tab1:
                report_function(df)
            
            with tab2:
                comparison_function(df)
            
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")