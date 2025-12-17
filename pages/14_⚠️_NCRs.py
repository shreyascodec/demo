"""
NCRs page - Non-Conformance Report management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="NCRs", page_icon="⚠️", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("⚠️ Non-Conformance Reports (NCRs)")
st.markdown("Track and manage non-conformances and corrective actions")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Create NCR", width="stretch"):
        st.session_state.show_add_ncr = True

# Add NCR form
if st.session_state.get('show_add_ncr', False):
    with st.form("add_ncr_form"):
        st.subheader("Create New NCR")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ncr_title = st.text_input("NCR Title *", placeholder="Brief description of non-conformance")
            severity = st.selectbox("Severity", ["minor", "major", "critical"])
            category = st.selectbox("Category", [
                "Documentation",
                "Process",
                "Equipment",
                "Personnel",
                "Quality",
                "Safety",
                "Other"
            ])
        
        with col2:
            status = st.selectbox("Status", [
                "open",
                "investigating",
                "action_taken",
                "closed"
            ])
            reported_by = st.text_input("Reported By", placeholder="Your name")
            detected_date = st.date_input("Detection Date", value=datetime.now())
        
        description = st.text_area("Description *", placeholder="Detailed description of the non-conformance...")
        root_cause = st.text_area("Root Cause Analysis", placeholder="Analysis of the root cause...")
        corrective_action = st.text_area("Corrective Action", placeholder="Actions taken or proposed...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create NCR", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if ncr_title and description:
                new_ncr = {
                    'title': ncr_title,
                    'description': description,
                    'severity': severity,
                    'category': category,
                    'status': status,
                    'reported_by': reported_by,
                    'detected_date': detected_date.strftime('%Y-%m-%d'),
                    'root_cause': root_cause,
                    'corrective_action': corrective_action,
                }
                ds.add_ncr(new_ncr)
                st.success(f"✅ NCR '{ncr_title}' created successfully!")
                st.session_state.show_add_ncr = False
                st.rerun()
            else:
                st.error("Please fill in all required fields")
        
        if cancel:
            st.session_state.show_add_ncr = False
            st.rerun()

st.markdown("---")

# Statistics
ncrs = ds.get_all_ncrs()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total NCRs", len(ncrs))

with col2:
    open_ncrs = len([n for n in ncrs if n.get('status') == 'open'])
    st.metric("Open", open_ncrs)

with col3:
    critical = len([n for n in ncrs if n.get('severity') == 'critical'])
    st.metric("Critical", critical)

with col4:
    closed = len([n for n in ncrs if n.get('status') == 'closed'])
    st.metric("Closed", closed)

st.markdown("---")

# Display NCRs
if ncrs:
    st.subheader(f"NCR List ({len(ncrs)} NCRs)")
    
    for ncr in ncrs:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### NCR-{ncr['id']:04d}: {ncr['title']}")
                st.markdown(f"**Category:** {ncr.get('category', 'N/A')}")
                if ncr.get('description'):
                    st.markdown(f"*{ncr['description'][:100]}...*" if len(ncr.get('description', '')) > 100 else f"*{ncr.get('description')}*")
            
            with col2:
                st.markdown(f"**Reported By:** {ncr.get('reported_by', 'N/A')}")
                st.markdown(f"**Detected:** {ncr.get('detected_date', 'N/A')}")
                st.markdown(f"**Status:** {ncr.get('status', 'open').upper()}")
            
            with col3:
                severity = ncr.get('severity', 'minor')
                if severity == 'critical':
                    st.error("CRITICAL")
                elif severity == 'major':
                    st.warning("MAJOR")
                else:
                    st.info("MINOR")
                
                if st.button("View", key=f"view_ncr_{ncr['id']}", width="stretch"):
                    st.info(f"NCR details for NCR-{ncr['id']:04d}")
            
            st.markdown("---")
else:
    st.info("No NCRs recorded. This is good news!")

# Critical NCRs alert
critical_ncrs = [n for n in ncrs if n.get('severity') == 'critical' and n.get('status') != 'closed']
if critical_ncrs:
    st.error(f"⚠️ Attention: {len(critical_ncrs)} critical NCR(s) require immediate action!")

# Footer
st.markdown("---")
st.caption("💡 Tip: Document non-conformances promptly and implement corrective actions to prevent recurrence.")

