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

# Test plan details - Display prominently before the list if selected
if st.session_state.get('selected_test_plan'):
    st.markdown("---")
    st.markdown("## 📋 Test Plan Details")
    
    tp_id = st.session_state.selected_test_plan
    tp = next((t for t in test_plans if t['id'] == tp_id), None)
    
    if tp:
        # Get related data
        project = ds.get_project_by_id(tp.get('project_id'))
        test_executions = ds.get_test_executions_by_test_plan(tp_id)
        test_results = ds.get_test_results_by_test_plan(tp_id)
        
        # Display details in a container instead of expander for better visibility
        with st.container():
            st.markdown(f"### 🧪 {tp['name']}")
            
            # Close button at top
            if st.button("❌ Close Details", key=f"close_top_{tp_id}"):
                st.session_state.selected_test_plan = None
                st.rerun()
            
            st.markdown("---")
            # Main Information Section
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Test Plan Information")
                st.write(f"**Name:** {tp['name']}")
                st.write(f"**Project:** {tp['project_name']}")
                if project:
                    st.write(f"**Project Code:** {project.get('code', 'N/A')}")
                st.write(f"**Test Type:** {tp['test_type']}")
                st.write(f"**Status:** {tp['status']}")
                st.write(f"**Description:** {tp.get('description', 'No description')}")
                if tp.get('created_at'):
                    st.write(f"**Created:** {tp['created_at']}")
            
            with col2:
                st.markdown("#### Assignment & Timeline")
                st.write(f"**Assigned Engineer:** {tp.get('assigned_engineer_name', 'Unassigned')}")
                st.write(f"**Planned Start:** {tp.get('planned_start_date', 'N/A')}")
                st.write(f"**Planned End:** {tp.get('planned_end_date', 'N/A')}")
                st.write(f"**Actual Start:** {tp.get('actual_start_date', 'Not started')}")
                st.write(f"**Actual End:** {tp.get('actual_end_date', 'Not completed')}")
                
                # Calculate duration if dates are available
                if tp.get('actual_start_date') and tp.get('actual_end_date'):
                    try:
                        start = datetime.strptime(tp['actual_start_date'], '%Y-%m-%d')
                        end = datetime.strptime(tp['actual_end_date'], '%Y-%m-%d')
                        duration = (end - start).days
                        st.write(f"**Duration:** {duration} days")
                    except:
                        pass
            
            st.markdown("---")
            
            # Project Information
            if project:
                st.markdown("#### Related Project Information")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Customer:** {project.get('client_name', 'N/A')}")
                    st.write(f"**Project Status:** {project.get('status', 'N/A').upper()}")
                
                with col2:
                    st.write(f"**Start Date:** {project.get('start_date', 'N/A')}")
                    st.write(f"**End Date:** {project.get('end_date', 'N/A')}")
                
                with col3:
                    st.write(f"**Estimated Cost:** ₹{project.get('estimated_cost', 0):,}")
                    st.write(f"**Actual Cost:** ₹{project.get('actual_cost', 0):,}")
            
            st.markdown("---")
            
            # Test Executions Section
            st.markdown("#### Test Executions")
            if test_executions:
                st.write(f"**Total Executions:** {len(test_executions)}")
                
                # Execution statistics
                exec_col1, exec_col2, exec_col3, exec_col4 = st.columns(4)
                with exec_col1:
                    completed_execs = len([e for e in test_executions if e.get('status') == 'Completed'])
                    st.metric("Completed", completed_execs)
                with exec_col2:
                    running_execs = len([e for e in test_executions if e.get('status') == 'running'])
                    st.metric("Running", running_execs)
                with exec_col3:
                    pending_execs = len([e for e in test_executions if e.get('status') == 'pending'])
                    st.metric("Pending", pending_execs)
                with exec_col4:
                    passed_execs = len([e for e in test_executions if e.get('result') == 'Pass'])
                    st.metric("Passed", passed_execs)
                
                # Execution list
                st.markdown("**Execution History:**")
                for execution in test_executions:
                    with st.container():
                        exec_col1, exec_col2, exec_col3 = st.columns([3, 2, 1])
                        
                        with exec_col1:
                            st.write(f"**{execution.get('test_name', f'Execution #{execution['id']}')}**")
                            if execution.get('started_at'):
                                st.caption(f"Started: {execution['started_at']}")
                        
                        with exec_col2:
                            status = execution.get('status', 'pending')
                            if status == 'Completed':
                                st.success(f"Status: {status}")
                            elif status == 'running':
                                st.warning(f"Status: {status}")
                            else:
                                st.info(f"Status: {status}")
                            
                            if execution.get('result'):
                                result_color = 'success' if execution['result'] == 'Pass' else 'error'
                                if execution['result'] == 'Pass':
                                    st.success(f"Result: {execution['result']}")
                                else:
                                    st.error(f"Result: {execution['result']}")
                        
                        with exec_col3:
                            if execution.get('ended_at'):
                                st.caption(f"Ended: {execution['ended_at']}")
                        
                        st.markdown("---")
            else:
                st.info("No test executions recorded for this test plan yet.")
            
            # Test Results Section
            st.markdown("#### Test Results")
            if test_results:
                st.write(f"**Total Results:** {len(test_results)}")
                
                # Results statistics
                result_col1, result_col2 = st.columns(2)
                with result_col1:
                    passed_results = len([r for r in test_results if r.get('pass_fail') == 'Pass'])
                    st.metric("Passed", passed_results)
                with result_col2:
                    failed_results = len([r for r in test_results if r.get('pass_fail') == 'Fail'])
                    st.metric("Failed", failed_results)
                
                # Results list
                st.markdown("**Test Results:**")
                for result in test_results:
                    with st.container():
                        result_col1, result_col2, result_col3 = st.columns([3, 1, 1])
                        
                        with result_col1:
                            st.write(f"**{result.get('test_name', 'N/A')}**")
                            st.caption(f"Type: {result.get('test_type', 'N/A')}")
                            if result.get('created_at'):
                                st.caption(f"Created: {result['created_at']}")
                        
                        with result_col2:
                            pass_fail = result.get('pass_fail', 'N/A')
                            if pass_fail == 'Pass':
                                st.success("PASS")
                            elif pass_fail == 'Fail':
                                st.error("FAIL")
                            else:
                                st.info(pass_fail)
                        
                        with result_col3:
                            st.caption(f"Result ID: #{result['id']}")
                        
                        st.markdown("---")
            else:
                st.info("No test results available for this test plan yet.")
            
            st.markdown("---")
            
            # Actions
            st.markdown("#### Actions")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if tp['status'] == 'Draft':
                    if st.button("▶️ Start Test", key=f"start_{tp_id}", width="stretch"):
                        ds.update_test_plan(tp['id'], {
                            'status': 'InProgress',
                            'actual_start_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        st.success("Test plan started!")
                        st.rerun()
            
            with col2:
                if tp['status'] == 'InProgress':
                    if st.button("✅ Complete Test", key=f"complete_{tp_id}", width="stretch"):
                        ds.update_test_plan(tp['id'], {
                            'status': 'Completed',
                            'actual_end_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        st.success("Test plan completed!")
                        st.rerun()
            
            with col3:
                if st.button("⚗️ View Executions", key=f"executions_{tp_id}", width="stretch"):
                    st.switch_page("pages/08_⚗️_Test_Executions.py")
            
            with col4:
                if st.button("❌ Close Details", key=f"close_{tp_id}", width="stretch"):
                    st.session_state.selected_test_plan = None
                    st.rerun()
    else:
        st.error(f"Test plan with ID {tp_id} not found.")
        if st.button("Close"):
            st.session_state.selected_test_plan = None
            st.rerun()
    
    st.markdown("---")

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

# Footer
st.markdown("---")
st.caption("💡 Tip: Create test plans for projects to organize and track testing activities.")
