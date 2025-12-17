"""
Certifications page - Certification management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="Certifications", page_icon="🏆", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("🏆 Certifications")
st.markdown("Track certifications and accreditations")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Add Certification", width="stretch"):
        st.session_state.show_add_cert = True

# Add certification form
if st.session_state.get('show_add_cert', False):
    with st.form("add_cert_form"):
        st.subheader("Add New Certification")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cert_name = st.text_input("Certification Name *", placeholder="e.g., ISO 9001:2015")
            cert_type = st.selectbox("Type", [
                "Quality Management",
                "Environmental Management",
                "Safety Management",
                "Testing Accreditation",
                "Calibration Accreditation",
                "Other"
            ])
            issued_by = st.text_input("Issued By", placeholder="Certifying body")
        
        with col2:
            cert_number = st.text_input("Certificate Number", placeholder="Certificate/License number")
            issue_date = st.date_input("Issue Date", value=datetime.now())
            expiry_date = st.date_input("Expiry Date", value=datetime.now() + timedelta(days=365*3))
        
        status = st.selectbox("Status", ["active", "expired", "suspended", "pending_renewal"])
        scope = st.text_area("Scope", placeholder="Scope and coverage of the certification...")
        notes = st.text_area("Notes", placeholder="Additional notes or requirements...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Add Certification", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if cert_name:
                new_cert = {
                    'name': cert_name,
                    'cert_type': cert_type,
                    'cert_number': cert_number,
                    'issued_by': issued_by,
                    'issue_date': issue_date.strftime('%Y-%m-%d'),
                    'expiry_date': expiry_date.strftime('%Y-%m-%d'),
                    'status': status,
                    'scope': scope,
                    'notes': notes,
                }
                ds.add_certification(new_cert)
                st.success(f"✅ Certification '{cert_name}' added successfully!")
                st.session_state.show_add_cert = False
                st.rerun()
            else:
                st.error("Please provide certification name")
        
        if cancel:
            st.session_state.show_add_cert = False
            st.rerun()

st.markdown("---")

# Statistics
certifications = ds.get_all_certifications()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Certifications", len(certifications))

with col2:
    active = len([c for c in certifications if c.get('status') == 'active'])
    st.metric("Active", active)

with col3:
    # Calculate expiring soon (within 90 days)
    expiring_soon = 0
    today = datetime.now()
    for cert in certifications:
        if cert.get('expiry_date'):
            try:
                expiry = datetime.strptime(cert['expiry_date'], '%Y-%m-%d')
                if 0 <= (expiry - today).days <= 90:
                    expiring_soon += 1
            except:
                pass
    st.metric("Expiring Soon", expiring_soon)

with col4:
    expired = len([c for c in certifications if c.get('status') == 'expired'])
    st.metric("Expired", expired)

st.markdown("---")

# Display certifications
if certifications:
    st.subheader(f"Certification List ({len(certifications)} certifications)")
    
    for cert in certifications:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### 🏆 {cert['name']}")
                st.markdown(f"**Type:** {cert.get('cert_type', 'N/A')}")
                st.markdown(f"**Issued By:** {cert.get('issued_by', 'N/A')}")
                st.markdown(f"**Certificate #:** {cert.get('cert_number', 'N/A')}")
            
            with col2:
                st.markdown(f"**Issue Date:** {cert.get('issue_date', 'N/A')}")
                st.markdown(f"**Expiry Date:** {cert.get('expiry_date', 'N/A')}")
                
                # Calculate days until expiry
                if cert.get('expiry_date'):
                    try:
                        expiry = datetime.strptime(cert['expiry_date'], '%Y-%m-%d')
                        days_left = (expiry - datetime.now()).days
                        if days_left > 0:
                            if days_left <= 90:
                                st.warning(f"⚠️ Expires in {days_left} days")
                            else:
                                st.info(f"Valid for {days_left} days")
                        else:
                            st.error("❌ Expired")
                    except:
                        pass
            
            with col3:
                status = cert.get('status', 'active')
                if status == 'active':
                    st.success("ACTIVE")
                elif status == 'expired':
                    st.error("EXPIRED")
                elif status == 'suspended':
                    st.warning("SUSPENDED")
                else:
                    st.info("PENDING RENEWAL")
                
                if st.button("View", key=f"view_cert_{cert['id']}", width="stretch"):
                    st.info(f"Certificate details for {cert['name']}")
            
            st.markdown("---")
else:
    st.info("No certifications recorded. Add your laboratory certifications to track their status.")

# Renewal reminders
expiring_certs = []
today = datetime.now()
for cert in certifications:
    if cert.get('expiry_date') and cert.get('status') == 'active':
        try:
            expiry = datetime.strptime(cert['expiry_date'], '%Y-%m-%d')
            days_left = (expiry - today).days
            if 0 <= days_left <= 90:
                expiring_certs.append((cert, days_left))
        except:
            pass

if expiring_certs:
    st.warning("### 📅 Renewal Reminders")
    st.markdown("The following certifications require renewal soon:")
    for cert, days_left in expiring_certs:
        st.markdown(f"- **{cert['name']}** - Expires in **{days_left} days**")

# Footer
st.markdown("---")
st.caption("💡 Tip: Keep your certifications up-to-date to maintain compliance and credibility.")

