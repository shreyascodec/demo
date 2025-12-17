"""
Test Executions page - Track test execution progress
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="Test Executions", page_icon="⚗️", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("⚗️ Test Executions")
st.markdown("Monitor and manage test execution activities")

# Statistics
test_executions = ds.get_all_test_executions()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Executions", len(test_executions))

with col2:
    running = len([te for te in test_executions if te.get('status') == 'running'])
    st.metric("Running", running)

with col3:
    completed = len([te for te in test_executions if te.get('status') == 'completed'])
    st.metric("Completed", completed)

with col4:
    pending = len([te for te in test_executions if te.get('status') == 'pending'])
    st.metric("Pending", pending)

st.markdown("---")

# Display available test plans
st.subheader("Available Test Plans")
st.markdown("Test plans that can be executed:")

test_plans = ds.get_all_test_plans()
executable_plans = [tp for tp in test_plans if tp['status'] in ['Approved', 'InProgress']]

if executable_plans:
    for tp in executable_plans:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**{tp['name']}**")
                st.markdown(f"Project: {tp['project_name']}")
            
            with col2:
                st.markdown(f"Type: {tp['test_type']}")
                st.markdown(f"Engineer: {tp.get('assigned_engineer_name', 'Unassigned')}")
            
            with col3:
                st.markdown(f"Status: {tp['status']}")
                if st.button("Execute", key=f"exec_{tp['id']}", width="stretch"):
                    st.info(f"Execution started for: {tp['name']}")
            
            st.markdown("---")
else:
    st.info("No test plans available for execution. Create and approve test plans first.")

# Display executions
st.markdown("---")
st.subheader("Execution History")

if test_executions:
    for execution in test_executions:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### Execution #{execution['id']}")
                st.markdown(f"**Test:** {execution.get('test_name', 'N/A')}")
            
            with col2:
                st.markdown(f"**Started:** {execution.get('start_time', 'N/A')}")
                st.markdown(f"**Duration:** {execution.get('duration', 'N/A')}")
            
            with col3:
                status = execution.get('status', 'pending')
                if status == 'completed':
                    st.success("COMPLETED")
                elif status == 'running':
                    st.warning("RUNNING")
                else:
                    st.info("PENDING")
            
            st.markdown("---")
else:
    st.info("No test executions recorded yet. Start executing test plans to see them here.")

# Footer
st.markdown("---")
st.caption("💡 Tip: Execute approved test plans and track their progress here.")
