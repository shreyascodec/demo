"""
Projects page - Project management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService
from services.chart_service import ChartService

st.set_page_config(page_title="Projects", page_icon="📁", layout="wide")

# Initialize services
ds = DataService()
cs = ChartService()

# Header
st.title("📁 Projects")
st.markdown("Manage and track all your lab testing projects")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Create New Project", width="stretch"):
        st.session_state.show_add_project = True

# Add project form
if st.session_state.get('show_add_project', False):
    with st.form("add_project_form"):
        st.subheader("Create New Project")
        
        customers = ds.get_all_customers()
        customer_options = {f"{c['company_name']}": c for c in customers}
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name *", placeholder="Enter project name")
            selected_customer = st.selectbox("Customer *", options=list(customer_options.keys()))
            status = st.selectbox("Status", ["pending", "active", "completed", "on_hold"])
        
        with col2:
            project_code = st.text_input("Project Code *", placeholder="PROJ-2024-XXX")
            estimated_cost = st.number_input("Estimated Cost (₹)", min_value=0.0, value=50000.0, step=1000.0)
            
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now())
        
        with col2:
            end_date = st.date_input("End Date", value=datetime.now() + timedelta(days=30))
        
        description = st.text_area("Project Description", placeholder="Detailed description of the project scope and objectives...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Project", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if project_name and project_code and selected_customer:
                customer = customer_options[selected_customer]
                new_project = {
                    'code': project_code,
                    'name': project_name,
                    'client_id': customer['id'],
                    'client_name': customer['company_name'],
                    'description': description,
                    'status': status,
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'estimated_cost': estimated_cost,
                    'actual_cost': 0.0,
                }
                ds.add_project(new_project)
                st.success(f"✅ Project '{project_name}' created successfully!")
                st.session_state.show_add_project = False
                st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *)")
        
        if cancel:
            st.session_state.show_add_project = False
            st.rerun()

st.markdown("---")

# Statistics
projects = ds.get_all_projects()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Projects", len(projects))

with col2:
    active = len([p for p in projects if p['status'] == 'active'])
    st.metric("Active Projects", active)

with col3:
    completed = len([p for p in projects if p['status'] == 'completed'])
    st.metric("Completed", completed)

with col4:
    total_value = sum([p.get('estimated_cost', 0) for p in projects if p['status'] == 'active'])
    st.metric("Active Value", f"₹{total_value:,.0f}")

st.markdown("---")

# Filters
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_term = st.text_input("🔍 Search projects", placeholder="Search by name, code, or customer...")

with col2:
    status_filter = st.selectbox("Status", ["All", "pending", "active", "completed", "on_hold"])

with col3:
    sort_by = st.selectbox("Sort by", ["Created Date", "Start Date", "Name"])

# Apply filters
filtered_projects = projects

if search_term:
    filtered_projects = [p for p in filtered_projects if 
                        search_term.lower() in p.get('name', '').lower() or
                        search_term.lower() in p.get('code', '').lower() or
                        search_term.lower() in p.get('client_name', '').lower()]

if status_filter != "All":
    filtered_projects = [p for p in filtered_projects if p['status'] == status_filter]

def display_project_card(project, ds):
    """Display a project card"""
    with st.container():
        # Status badge
        status = project['status']
        if status == 'active':
            status_badge = "🟢 ACTIVE"
            status_color = "success"
        elif status == 'completed':
            status_badge = "✅ COMPLETED"
            status_color = "info"
        elif status == 'on_hold':
            status_badge = "⏸️ ON HOLD"
            status_color = "warning"
        else:
            status_badge = "🔵 PENDING"
            status_color = "secondary"
        
        st.markdown(f"### {project['name']}")
        st.markdown(f"**Code:** {project['code']}")
        st.markdown(f"**Customer:** {project['client_name']}")
        
        # Progress bar (mock)
        progress = 100 if status == 'completed' else (50 if status == 'active' else 0)
        st.progress(progress / 100)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Start:** {project.get('start_date', 'N/A')}")
            st.markdown(f"**Cost:** ₹{project.get('estimated_cost', 0):,}")
        
        with col2:
            st.markdown(f"**End:** {project.get('end_date', 'N/A')}")
            
            # Count test plans
            test_plans = ds.get_test_plans_by_project(project['id'])
            st.markdown(f"**Tests:** {len(test_plans)} plans")
        
        # Buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Details", key=f"details_{project['id']}", width="stretch"):
                st.session_state.selected_project = project['id']
                st.rerun()
        
        with col2:
            if st.button("🧪 Tests", key=f"tests_{project['id']}", width="stretch"):
                st.info(f"View test plans for project {project['code']}")
        
        with col3:
            if status == 'active':
                st.markdown(f":{status_color}[{status_badge}]")
            else:
                st.markdown(f"{status_badge}")
        
        st.markdown("---")

# Display projects
if filtered_projects:
    st.subheader(f"Project List ({len(filtered_projects)} results)")
    
    # Create grid layout
    for i in range(0, len(filtered_projects), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(filtered_projects):
                project = filtered_projects[i]
                display_project_card(project, ds)
        
        with col2:
            if i + 1 < len(filtered_projects):
                project = filtered_projects[i + 1]
                display_project_card(project, ds)
else:
    st.info("No projects found matching your criteria")

# Project details
if st.session_state.get('selected_project'):
    proj_id = st.session_state.selected_project
    project = ds.get_project_by_id(proj_id)
    
    if project:
        with st.expander(f"📁 Project Details: {project['name']}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Project Information")
                st.write(f"**Code:** {project['code']}")
                st.write(f"**Name:** {project['name']}")
                st.write(f"**Customer:** {project['client_name']}")
                st.write(f"**Status:** {project['status'].upper()}")
                st.write(f"**Description:** {project.get('description', 'No description')}")
            
            with col2:
                st.markdown("#### Timeline & Cost")
                st.write(f"**Start Date:** {project.get('start_date', 'N/A')}")
                st.write(f"**End Date:** {project.get('end_date', 'N/A')}")
                st.write(f"**Estimated Cost:** ₹{project.get('estimated_cost', 0):,}")
                st.write(f"**Actual Cost:** ₹{project.get('actual_cost', 0):,}")
                st.write(f"**Created:** {project.get('created_at', 'N/A')}")
            
            # Test plans
            st.markdown("#### Associated Test Plans")
            test_plans = ds.get_test_plans_by_project(proj_id)
            
            if test_plans:
                for tp in test_plans:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{tp['name']}** - {tp['test_type']}")
                    
                    with col2:
                        st.write(tp['status'])
                    
                    with col3:
                        st.write(tp.get('assigned_engineer_name', 'Unassigned'))
            else:
                st.info("No test plans created for this project yet")
            
            # Actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🧪 Create Test Plan", width="stretch"):
                    st.switch_page("pages/07_🧪_Test_Plans.py")
            
            with col2:
                if st.button("📊 View Reports", width="stretch"):
                    st.switch_page("pages/12_📑_Reports.py")
            
            with col3:
                if st.button("Close Details"):
                    st.session_state.selected_project = None
                    st.rerun()

# Footer
st.markdown("---")
st.caption("💡 Tip: Create test plans for your projects to track testing progress and results.")

