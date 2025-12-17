"""
Audits page - Audit management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="Audits", page_icon="🔍", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("🔍 Audits")
st.markdown("Schedule and manage laboratory audits")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Schedule Audit", width="stretch"):
        st.session_state.show_add_audit = True

# Add audit form
if st.session_state.get('show_add_audit', False):
    with st.form("add_audit_form"):
        st.subheader("Schedule New Audit")
        
        col1, col2 = st.columns(2)
        
        with col1:
            audit_name = st.text_input("Audit Name *", placeholder="Enter audit name")
            audit_type = st.selectbox("Audit Type", [
                "Internal Audit",
                "External Audit",
                "Surveillance Audit",
                "Compliance Audit",
                "Process Audit"
            ])
            auditor = st.text_input("Auditor", placeholder="Auditor name")
        
        with col2:
            scheduled_date = st.date_input("Scheduled Date", value=datetime.now() + timedelta(days=7))
            status = st.selectbox("Status", ["scheduled", "in_progress", "completed", "pending_action"])
            department = st.text_input("Department", placeholder="Department/Area")
        
        scope = st.text_area("Audit Scope", placeholder="Define the scope and objectives of the audit...")
        findings = st.text_area("Findings", placeholder="Audit findings (can be updated later)...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Schedule Audit", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if audit_name and audit_type:
                new_audit = {
                    'name': audit_name,
                    'audit_type': audit_type,
                    'auditor': auditor,
                    'scheduled_date': scheduled_date.strftime('%Y-%m-%d'),
                    'status': status,
                    'department': department,
                    'scope': scope,
                    'findings': findings,
                }
                ds.add_audit(new_audit)
                st.success(f"✅ Audit '{audit_name}' scheduled successfully!")
                st.session_state.show_add_audit = False
                st.rerun()
            else:
                st.error("Please fill in all required fields")
        
        if cancel:
            st.session_state.show_add_audit = False
            st.rerun()

st.markdown("---")

# Statistics
audits = ds.get_all_audits()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Audits", len(audits))

with col2:
    scheduled = len([a for a in audits if a.get('status') == 'scheduled'])
    st.metric("Scheduled", scheduled)

with col3:
    in_progress = len([a for a in audits if a.get('status') == 'in_progress'])
    st.metric("In Progress", in_progress)

with col4:
    completed = len([a for a in audits if a.get('status') == 'completed'])
    st.metric("Completed", completed)

st.markdown("---")

# Display audits
if audits:
    st.subheader(f"Audit List ({len(audits)} audits)")
    
    for audit in audits:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### {audit['name']}")
                st.markdown(f"**Type:** {audit.get('audit_type', 'N/A')}")
                st.markdown(f"**Department:** {audit.get('department', 'N/A')}")
                if audit.get('scope'):
                    st.markdown(f"*{audit['scope'][:80]}...*" if len(audit.get('scope', '')) > 80 else f"*{audit.get('scope')}*")
            
            with col2:
                st.markdown(f"**Auditor:** {audit.get('auditor', 'TBD')}")
                st.markdown(f"**Scheduled:** {audit.get('scheduled_date', 'N/A')}")
            
            with col3:
                status = audit.get('status', 'scheduled')
                if status == 'scheduled':
                    st.info("SCHEDULED")
                elif status == 'in_progress':
                    st.warning("IN PROGRESS")
                elif status == 'completed':
                    st.success("COMPLETED")
                else:
                    st.warning("PENDING ACTION")
                
                if st.button("View", key=f"view_audit_{audit['id']}", width="stretch"):
                    st.info(f"Audit details for {audit['name']}")
            
            st.markdown("---")
else:
    st.info("No audits scheduled. Schedule your first audit to ensure compliance!")

# Upcoming audits reminder
upcoming = [a for a in audits if a.get('status') == 'scheduled']
if upcoming:
    st.info(f"📅 You have {len(upcoming)} upcoming audit(s) scheduled.")

# Footer
st.markdown("---")
st.caption("💡 Tip: Regular audits help maintain compliance and identify areas for improvement.")

