"""
Reports page - Generate and view reports
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService
from services.chart_service import ChartService

st.set_page_config(page_title="Reports", page_icon="📑", layout="wide")

# Initialize services
ds = DataService()
cs = ChartService()

# Header
st.title("📑 Reports")
st.markdown("Generate comprehensive reports and analytics")

# Report generation section
st.subheader("📊 Generate New Report")

col1, col2, col3 = st.columns(3)

with col1:
    report_type = st.selectbox("Report Type", [
        "Project Summary",
        "Test Results Summary",
        "Customer Activity",
        "Monthly Performance",
        "Test Plan Status",
        "Financial Summary"
    ])

with col2:
    date_range = st.selectbox("Date Range", [
        "Last Week",
        "Last Month",
        "Last Quarter",
        "Last Year",
        "Custom Range"
    ])

with col3:
    format_type = st.selectbox("Export Format", ["PDF", "Excel", "CSV"])

if st.button("🔄 Generate Report", width="stretch"):
    with st.spinner("Generating report..."):
        st.success(f"✅ {report_type} report generated successfully!")
        st.download_button(
            label="📥 Download Report",
            data="Sample report data",
            file_name=f"report_{datetime.now().strftime('%Y%m%d')}.{format_type.lower()}",
            mime="application/pdf"
        )

st.markdown("---")

# Quick Statistics Dashboard
st.subheader("📈 Quick Statistics")

stats = ds.get_dashboard_stats()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Projects", stats['total_projects'])

with col2:
    st.metric("Active Projects", stats['active_projects'])

with col3:
    st.metric("Completed Tests", stats['completed_tests'])

with col4:
    st.metric("Total Customers", stats['total_customers'])

st.markdown("---")

# Project Performance Report
st.subheader("📊 Project Performance")

projects = ds.get_all_projects()

if projects:
    # Create DataFrame
    project_data = []
    for p in projects:
        project_data.append({
            'Code': p['code'],
            'Name': p['name'],
            'Customer': p['client_name'],
            'Status': p['status'].upper(),
            'Estimated Cost': f"₹{p.get('estimated_cost', 0):,.0f}",
            'Start Date': p.get('start_date', 'N/A'),
            'End Date': p.get('end_date', 'N/A'),
        })
    
    df = pd.DataFrame(project_data)
    st.dataframe(df, width="stretch", hide_index=True)
    
    # Export option
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Export Project Data (CSV)",
        data=csv,
        file_name=f"projects_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
else:
    st.info("No project data available")

st.markdown("---")

# Test Plans Summary
st.subheader("🧪 Test Plans Summary")

test_plans = ds.get_all_test_plans()

if test_plans:
    # Status distribution
    status_counts = {}
    for tp in test_plans:
        status = tp['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_data = [{'status': k, 'count': v} for k, v in status_counts.items()]
        fig = cs.create_pie_chart(status_data, 'count', 'status', 'Test Plan Status Distribution')
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        # Type distribution
        type_counts = {}
        for tp in test_plans:
            test_type = tp['test_type']
            type_counts[test_type] = type_counts.get(test_type, 0) + 1
        
        type_data = [{'type': k, 'count': v} for k, v in type_counts.items()]
        fig = cs.create_bar_chart(type_data, 'type', 'count', 'Test Plans by Type', '#10b981')
        st.plotly_chart(fig, width="stretch")
else:
    st.info("No test plan data available")

st.markdown("---")

# Customer Summary
st.subheader("👥 Customer Summary")

customers = ds.get_all_customers()

if customers:
    col1, col2, col3 = st.columns([2, 1, 1])
    
    for customer in customers[:5]:
        with col1:
            st.markdown(f"**{customer['company_name']}**")
        
        with col2:
            # Count customer projects
            customer_projects = [p for p in projects if p['client_id'] == customer['id']]
            st.markdown(f"{len(customer_projects)} projects")
        
        with col3:
            st.markdown(customer['status'].upper())
        
        st.markdown("---")
else:
    st.info("No customer data available")

# Report History (mock)
st.subheader("📜 Report History")

report_history = [
    {"name": "Monthly Performance Report", "date": "2024-01-15", "type": "PDF"},
    {"name": "Project Summary", "date": "2024-01-10", "type": "Excel"},
    {"name": "Test Results Analysis", "date": "2024-01-05", "type": "PDF"},
]

for report in report_history:
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        st.markdown(f"📄 **{report['name']}**")
    
    with col2:
        st.markdown(f"Generated: {report['date']}")
    
    with col3:
        st.markdown(report['type'])
        if st.button("View", key=f"view_{report['name']}", width="stretch"):
            st.info(f"Opening {report['name']}")
    
    st.markdown("---")

# Footer
st.markdown("---")
st.caption("💡 Tip: Generate reports regularly to track progress and make data-driven decisions.")

