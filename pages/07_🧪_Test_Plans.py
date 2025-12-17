"""
Test Plans page - Test planning and management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="Test Plans", page_icon="🧪", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("🧪 Test Plans")
st.markdown("Plan and manage all testing activities")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Create Test Plan", width="stretch"):
        st.session_state.show_add_test_plan = True

# Add test plan form
if st.session_state.get('show_add_test_plan', False):
    with st.form("add_test_plan_form"):
        st.subheader("Create New Test Plan")
        
        projects = ds.get_all_projects()
        project_options = {f"{p['code']} - {p['name']}": p for p in projects if p['status'] in ['active', 'pending']}
        
        col1, col2 = st.columns(2)
        
        with col1:
            if project_options:
                selected_project_str = st.selectbox("Project *", options=list(project_options.keys()))
                selected_project = project_options[selected_project_str]
            else:
                st.warning("No active projects available. Create a project first.")
                selected_project = None
            
            test_plan_name = st.text_input("Test Plan Name *", placeholder="Enter test plan name")
            test_type = st.selectbox("Test Type *", ["EMC", "RF", "Safety", "Environmental"])
        
        with col2:
            status = st.selectbox("Status", ["Draft", "InProgress", "Completed", "Approved"])
            engineer = st.text_input("Assigned Engineer", placeholder="Engineer name")
        
        col1, col2 = st.columns(2)
        
        with col1:
            planned_start = st.date_input("Planned Start Date", value=datetime.now())
        
        with col2:
            planned_end = st.date_input("Planned End Date", value=datetime.now() + timedelta(days=14))
        
        description = st.text_area("Description", placeholder="Detailed description of the test plan...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Test Plan", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if selected_project and test_plan_name and test_type:
                new_test_plan = {
                    'project_id': selected_project['id'],
                    'project_name': selected_project['name'],
                    'name': test_plan_name,
                    'description': description,
                    'test_type': test_type,
                    'status': status,
                    'assigned_engineer_name': engineer if engineer else 'Unassigned',
                    'planned_start_date': planned_start.strftime('%Y-%m-%d'),
                    'planned_end_date': planned_end.strftime('%Y-%m-%d'),
                }
                ds.add_test_plan(new_test_plan)
                st.success(f"✅ Test plan '{test_plan_name}' created successfully!")
                st.session_state.show_add_test_plan = False
                st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *)")
        
        if cancel:
            st.session_state.show_add_test_plan = False
            st.rerun()

st.markdown("---")

# Statistics
test_plans = ds.get_all_test_plans()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Test Plans", len(test_plans))

with col2:
    in_progress = len([tp for tp in test_plans if tp['status'] == 'InProgress'])
    st.metric("In Progress", in_progress)

with col3:
    completed = len([tp for tp in test_plans if tp['status'] == 'Completed'])
    st.metric("Completed", completed)

with col4:
    approved = len([tp for tp in test_plans if tp['status'] == 'Approved'])
    st.metric("Approved", approved)

st.markdown("---")

# Filters
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_term = st.text_input("🔍 Search test plans", placeholder="Search by name or project...")

with col2:
    test_type_filter = st.selectbox("Test Type", ["All", "EMC", "RF", "Safety", "Environmental"])

with col3:
    status_filter = st.selectbox("Status", ["All", "Draft", "InProgress", "Completed", "Approved"])

# Apply filters
filtered_plans = test_plans

if search_term:
    filtered_plans = [tp for tp in filtered_plans if 
                     search_term.lower() in tp.get('name', '').lower() or
                     search_term.lower() in tp.get('project_name', '').lower()]

if test_type_filter != "All":
    filtered_plans = [tp for tp in filtered_plans if tp['test_type'] == test_type_filter]

if status_filter != "All":
    filtered_plans = [tp for tp in filtered_plans if tp['status'] == status_filter]

# Display test plans
if filtered_plans:
    st.subheader(f"Test Plan List ({len(filtered_plans)} results)")
    
    for tp in filtered_plans:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### {tp['name']}")
                st.markdown(f"**Project:** {tp['project_name']}")
                st.markdown(f"**Type:** {tp['test_type']}")
                if tp.get('description'):
                    st.markdown(f"*{tp['description'][:100]}...*" if len(tp.get('description', '')) > 100 else f"*{tp.get('description')}*")
            
            with col2:
                st.markdown(f"**Engineer:** {tp.get('assigned_engineer_name', 'Unassigned')}")
                st.markdown(f"**Start:** {tp.get('planned_start_date', 'N/A')}")
                st.markdown(f"**End:** {tp.get('planned_end_date', 'N/A')}")
            
            with col3:
                status = tp['status']
                if status == 'Draft':
                    st.info("DRAFT")
                elif status == 'InProgress':
                    st.warning("IN PROGRESS")
                elif status == 'Completed':
                    st.success("COMPLETED")
                else:
                    st.success("APPROVED")
                
                if st.button("View Details", key=f"view_tp_{tp['id']}", width="stretch"):
                    st.session_state.selected_test_plan = tp['id']
                    st.rerun()
            
            st.markdown("---")
else:
    st.info("No test plans found matching your criteria")

# Test plan details
if st.session_state.get('selected_test_plan'):
    tp_id = st.session_state.selected_test_plan
    tp = next((t for t in test_plans if t['id'] == tp_id), None)
    
    if tp:
        with st.expander(f"🧪 Test Plan Details: {tp['name']}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Test Plan Information")
                st.write(f"**Name:** {tp['name']}")
                st.write(f"**Project:** {tp['project_name']}")
                st.write(f"**Test Type:** {tp['test_type']}")
                st.write(f"**Status:** {tp['status']}")
                st.write(f"**Description:** {tp.get('description', 'No description')}")
            
            with col2:
                st.markdown("#### Assignment & Timeline")
                st.write(f"**Assigned Engineer:** {tp.get('assigned_engineer_name', 'Unassigned')}")
                st.write(f"**Planned Start:** {tp.get('planned_start_date', 'N/A')}")
                st.write(f"**Planned End:** {tp.get('planned_end_date', 'N/A')}")
                st.write(f"**Actual Start:** {tp.get('actual_start_date', 'Not started')}")
                st.write(f"**Actual End:** {tp.get('actual_end_date', 'Not completed')}")
            
            # Actions
            st.markdown("#### Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if tp['status'] == 'Draft':
                    if st.button("▶️ Start Test", width="stretch"):
                        ds.update_test_plan(tp['id'], {
                            'status': 'InProgress',
                            'actual_start_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        st.success("Test plan started!")
                        st.rerun()
            
            with col2:
                if tp['status'] == 'InProgress':
                    if st.button("✅ Complete Test", width="stretch"):
                        ds.update_test_plan(tp['id'], {
                            'status': 'Completed',
                            'actual_end_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        st.success("Test plan completed!")
                        st.rerun()
            
            with col3:
                if st.button("Close Details"):
                    st.session_state.selected_test_plan = None
                    st.rerun()

# Footer
st.markdown("---")
st.caption("💡 Tip: Create test plans for projects to organize and track testing activities.")
