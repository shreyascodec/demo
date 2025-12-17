"""
Dashboard page - Overview of lab management system
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService
from services.chart_service import ChartService

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Initialize services
ds = DataService()
cs = ChartService()

# Header
st.title("📊 Dashboard")
st.markdown("Real-time overview of your lab operations and key metrics")

# Get statistics
stats = ds.get_dashboard_stats()
projects = ds.get_all_projects()
test_plans = ds.get_all_test_plans()
test_results = ds.get_all_test_results()

# KPI Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Active Projects",
        value=stats['active_projects'],
        delta=f"{stats['total_projects']} total",
        delta_color="off"
    )

with col2:
    st.metric(
        label="Total Customers",
        value=stats['total_customers'],
        delta="Active",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="Test Plans",
        value=stats['total_test_plans'],
        delta=f"{stats['completed_tests']} completed",
        delta_color="off"
    )

with col4:
    st.metric(
        label="Pending RFQs",
        value=stats['pending_rfqs'],
        delta="Awaiting response",
        delta_color="inverse"
    )

st.markdown("---")

# Performance Metrics Row
st.subheader("📈 Performance Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    completion_rate = (stats['completed_tests'] / stats['total_test_plans'] * 100) if stats['total_test_plans'] > 0 else 0
    st.metric("Test Completion Rate", f"{completion_rate:.1f}%")
    st.progress(completion_rate / 100)

with col2:
    project_completion = (stats['completed_projects'] / stats['total_projects'] * 100) if stats['total_projects'] > 0 else 0
    st.metric("Project Completion", f"{project_completion:.1f}%")
    st.progress(project_completion / 100)

with col3:
    on_time_delivery = 85.0  # Mock metric
    st.metric("On-Time Delivery", f"{on_time_delivery:.1f}%")
    st.progress(on_time_delivery / 100)

with col4:
    avg_cycle_time = 12  # Mock metric in days
    st.metric("Avg Cycle Time", f"{avg_cycle_time} days")

st.markdown("---")

# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.subheader("Project Status Distribution")
    
    # Project status data
    status_data = [
        {'status': 'Active', 'count': stats['active_projects']},
        {'status': 'Completed', 'count': stats['completed_projects']},
        {'status': 'Pending', 'count': stats['total_projects'] - stats['active_projects'] - stats['completed_projects']},
    ]
    
    if sum(item['count'] for item in status_data) > 0:
        fig = cs.create_pie_chart(status_data, 'count', 'status', 'Project Status')
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No project data available")

with col2:
    st.subheader("Test Plans by Type")
    
    # Test type distribution
    test_types = {}
    for tp in test_plans:
        test_type = tp.get('test_type', 'Unknown')
        test_types[test_type] = test_types.get(test_type, 0) + 1
    
    if test_types:
        type_data = [{'type': k, 'count': v} for k, v in test_types.items()]
        fig = cs.create_bar_chart(type_data, 'type', 'count', 'Test Plans by Type', '#10b981')
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("No test plan data available")

st.markdown("---")

# Monthly Trends
st.subheader("📅 Monthly Trends")

# Generate mock monthly data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
monthly_data = []

for i, month in enumerate(months):
    projects_count = len([p for p in projects if p['status'] == 'active']) if i == len(months) - 1 else i + 1
    tests_count = len([tp for tp in test_plans if tp['status'] == 'InProgress']) if i == len(months) - 1 else i * 2
    completed_count = stats['completed_tests'] if i == len(months) - 1 else i
    
    monthly_data.append({
        'month': month,
        'projects': projects_count,
        'tests': tests_count,
        'completed': completed_count
    })

fig = cs.create_area_chart(monthly_data, 'month', ['projects', 'tests', 'completed'], 'Monthly Activity Trends')
st.plotly_chart(fig, width="stretch")

st.markdown("---")

# Recent Activities
st.subheader("🔔 Recent Activities")

activities = []

# Get recent projects
recent_projects = sorted(projects, key=lambda x: x.get('created_at', ''), reverse=True)[:3]
for proj in recent_projects:
    activities.append({
        'type': 'Project',
        'title': proj['name'],
        'status': proj['status'],
        'time': proj.get('created_at', 'Recently')
    })

# Get recent test plans
recent_plans = sorted(test_plans, key=lambda x: x.get('created_at', ''), reverse=True)[:3]
for plan in recent_plans:
    activities.append({
        'type': 'Test Plan',
        'title': plan['name'],
        'status': plan['status'],
        'time': plan.get('created_at', 'Recently')
    })

# Display activities
if activities:
    for activity in activities[:6]:
        col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
        
        with col1:
            if activity['type'] == 'Project':
                st.markdown("📁 **Project**")
            else:
                st.markdown("🧪 **Test Plan**")
        
        with col2:
            st.markdown(activity['title'])
        
        with col3:
            status = activity['status']
            if status == 'active':
                st.success(status.upper())
            elif status == 'completed' or status == 'Completed':
                st.info(status.upper())
            elif status == 'InProgress':
                st.warning('IN PROGRESS')
            else:
                st.markdown(status)
        
        with col4:
            st.markdown(f"*{activity['time']}*")
        
        st.markdown("---")
else:
    st.info("No recent activities")

# Quick Actions
st.markdown("---")
st.subheader("⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("➕ New Project", width="stretch"):
        st.switch_page("pages/05_📁_Projects.py")

with col2:
    if st.button("📋 View RFQs", width="stretch"):
        st.switch_page("pages/03_📋_RFQs.py")

with col3:
    if st.button("🧪 Test Plans", width="stretch"):
        st.switch_page("pages/07_🧪_Test_Plans.py")

with col4:
    if st.button("👥 Customers", width="stretch"):
        st.switch_page("pages/02_👥_Customers.py")

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M')}")

