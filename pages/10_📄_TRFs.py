"""
TRFs page - Test Request Forms management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="TRFs", page_icon="📄", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("📄 Test Request Forms (TRFs)")
st.markdown("Manage test request documentation")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Create TRF", width="stretch"):
        st.session_state.show_add_trf = True

# Add TRF form
if st.session_state.get('show_add_trf', False):
    with st.form("add_trf_form"):
        st.subheader("Create New TRF")
        
        projects = ds.get_all_projects()
        project_options = {f"{p['code']} - {p['name']}": p for p in projects}
        
        col1, col2 = st.columns(2)
        
        with col1:
            if project_options:
                selected_project_str = st.selectbox("Project *", options=list(project_options.keys()))
                selected_project = project_options[selected_project_str]
            else:
                st.warning("No projects available.")
                selected_project = None
            
            trf_number = st.text_input("TRF Number", placeholder="Auto-generated if empty")
        
        with col2:
            status = st.selectbox("Status", ["draft", "submitted", "approved", "rejected", "completed"])
            priority = st.selectbox("Priority", ["low", "normal", "high", "urgent"])
        
        requested_tests = st.multiselect(
            "Requested Tests",
            ["EMC Testing", "RF Testing", "Safety Testing", "Environmental Testing", "Certification"]
        )
        
        requirements = st.text_area("Requirements", placeholder="Test requirements and specifications...")
        notes = st.text_area("Notes", placeholder="Additional notes...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create TRF", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if selected_project and requested_tests:
                # Generate TRF number if not provided
                if not trf_number:
                    import random
                    trf_number = f"TRF-{datetime.now().year}-{random.randint(1000, 9999)}"
                
                new_trf = {
                    'project_id': selected_project['id'],
                    'project_name': selected_project['name'],
                    'trf_number': trf_number,
                    'requested_tests': requested_tests,
                    'requirements': requirements,
                    'notes': notes,
                    'status': status,
                    'priority': priority,
                }
                ds.add_trf(new_trf)
                st.success(f"✅ TRF '{trf_number}' created successfully!")
                st.session_state.show_add_trf = False
                st.rerun()
            else:
                st.error("Please fill in all required fields")
        
        if cancel:
            st.session_state.show_add_trf = False
            st.rerun()

st.markdown("---")

# Statistics
trfs = ds.get_all_trfs()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total TRFs", len(trfs))

with col2:
    pending = len([t for t in trfs if t.get('status') in ['draft', 'submitted']])
    st.metric("Pending", pending)

with col3:
    approved = len([t for t in trfs if t.get('status') == 'approved'])
    st.metric("Approved", approved)

with col4:
    completed = len([t for t in trfs if t.get('status') == 'completed'])
    st.metric("Completed", completed)

st.markdown("---")

# Display TRFs
if trfs:
    st.subheader(f"TRF List ({len(trfs)} TRFs)")
    
    # Filters
    statuses = ["All", "draft", "submitted", "approved", "rejected", "completed"]
    priorities = ["All", "low", "normal", "high", "urgent"]
    selected_status = st.selectbox("Filter by Status", statuses)
    selected_priority = st.selectbox("Filter by Priority", priorities)
    search_term = st.text_input("Search", placeholder="Search by TRF number, project, or test...")
    
    filtered = trfs
    if selected_status != "All":
        filtered = [t for t in filtered if t.get('status') == selected_status]
    if selected_priority != "All":
        filtered = [t for t in filtered if t.get('priority') == selected_priority]
    if search_term:
        s = search_term.lower()
        filtered = [
            t for t in filtered
            if s in t.get('trf_number', '').lower()
            or s in t.get('project_name', '').lower()
            or any(s in test.lower() for test in t.get('requested_tests', []))
        ]
    
    trfs = filtered
    
    for trf in trfs:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### {trf.get('trf_number', 'N/A')}")
                st.markdown(f"**Project:** {trf.get('project_name', 'N/A')}")
                st.markdown(f"**Tests:** {', '.join(trf.get('requested_tests', []))}")
            
            with col2:
                st.markdown(f"**Priority:** {trf.get('priority', 'normal').upper()}")
                st.markdown(f"**Created:** {trf.get('created_at', 'N/A')}")
            
            with col3:
                status = trf.get('status', 'draft')
                if status == 'draft':
                    st.info("DRAFT")
                elif status == 'submitted':
                    st.warning("SUBMITTED")
                elif status == 'approved':
                    st.success("APPROVED")
                elif status == 'completed':
                    st.success("COMPLETED")
                else:
                    st.error("REJECTED")
                
                if st.button("View", key=f"view_trf_{trf['id']}", width="stretch"):
                    st.info(f"TRF details for {trf.get('trf_number')}")
            
            st.markdown("---")
else:
    st.info("No TRFs created yet. Create your first TRF to get started!")

# Footer
st.markdown("---")
st.caption("💡 Tip: TRFs are used to formally request tests and track approval workflows.")

