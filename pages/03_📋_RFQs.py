"""
RFQs page - Request for Quotation management
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="RFQs", page_icon="📋", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("📋 Request for Quotations (RFQs)")
st.markdown("Manage customer quotation requests")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Add New RFQ", width="stretch"):
        st.session_state.show_add_rfq = True

# Add RFQ form
if st.session_state.get('show_add_rfq', False):
    with st.form("add_rfq_form"):
        st.subheader("Add New RFQ")
        
        customers = ds.get_all_customers()
        customer_options = {f"{c['company_name']}": c for c in customers}
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_customer = st.selectbox(
                "Customer *",
                options=list(customer_options.keys()),
                help="Select the customer requesting the quotation"
            )
            product = st.text_input("Product/Service *", placeholder="Enter product or service name")
        
        with col2:
            status = st.selectbox("Status", ["pending", "approved", "rejected"])
            received_date = st.date_input("Received Date", value=datetime.now())
        
        description = st.text_area("Description", placeholder="Detailed description of the request...")
        notes = st.text_area("Internal Notes", placeholder="Any internal notes or comments...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Add RFQ", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if selected_customer and product:
                customer = customer_options[selected_customer]
                new_rfq = {
                    'customer_id': customer['id'],
                    'customer_name': customer['company_name'],
                    'product': product,
                    'description': description,
                    'received_date': received_date.strftime('%Y-%m-%d'),
                    'status': status,
                    'notes': notes,
                }
                ds.add_rfq(new_rfq)
                st.success(f"✅ RFQ for '{product}' added successfully!")
                st.session_state.show_add_rfq = False
                st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *)")
        
        if cancel:
            st.session_state.show_add_rfq = False
            st.rerun()

st.markdown("---")

# Statistics
rfqs = ds.get_all_rfqs()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total RFQs", len(rfqs))

with col2:
    pending = len([r for r in rfqs if r['status'] == 'pending'])
    st.metric("Pending", pending)

with col3:
    approved = len([r for r in rfqs if r['status'] == 'approved'])
    st.metric("Approved", approved)

with col4:
    rejected = len([r for r in rfqs if r['status'] == 'rejected'])
    st.metric("Rejected", rejected)

st.markdown("---")

# Filters
col1, col2 = st.columns([3, 1])

with col1:
    search_term = st.text_input("🔍 Search RFQs", placeholder="Search by product, customer, or description...")

with col2:
    status_filter = st.selectbox("Filter by Status", ["All", "pending", "approved", "rejected"])

# Apply filters
filtered_rfqs = rfqs

if search_term:
    filtered_rfqs = [r for r in filtered_rfqs if 
                     search_term.lower() in r.get('product', '').lower() or
                     search_term.lower() in r.get('customer_name', '').lower() or
                     search_term.lower() in r.get('description', '').lower()]

if status_filter != "All":
    filtered_rfqs = [r for r in filtered_rfqs if r['status'] == status_filter]

# Display RFQs
if filtered_rfqs:
    st.subheader(f"RFQ List ({len(filtered_rfqs)} results)")
    
    for rfq in filtered_rfqs:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### RFQ #{rfq['id']:03d}")
                st.markdown(f"**Product:** {rfq['product']}")
                st.markdown(f"**Customer:** {rfq['customer_name']}")
                if rfq.get('description'):
                    st.markdown(f"*{rfq['description'][:100]}...*" if len(rfq.get('description', '')) > 100 else f"*{rfq.get('description')}*")
            
            with col2:
                st.markdown(f"**Received:** {rfq['received_date']}")
                if rfq.get('notes'):
                    st.markdown(f"**Notes:** {rfq['notes'][:80]}..." if len(rfq.get('notes', '')) > 80 else rfq['notes'])
            
            with col3:
                status = rfq['status']
                if status == 'pending':
                    st.warning("PENDING")
                elif status == 'approved':
                    st.success("APPROVED")
                else:
                    st.error("REJECTED")
                
                # Action buttons
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button("📄 Details", key=f"details_{rfq['id']}", width="stretch"):
                        st.session_state.selected_rfq = rfq['id']
                        st.rerun()
                
                with col_b:
                    if status == 'pending' and st.button("✓ Approve", key=f"approve_{rfq['id']}", width="stretch"):
                        ds.update_rfq(rfq['id'], {'status': 'approved'})
                        st.success("RFQ approved!")
                        st.rerun()
            
            st.markdown("---")
else:
    st.info("No RFQs found matching your criteria")

# RFQ details
if st.session_state.get('selected_rfq'):
    rfq_id = st.session_state.selected_rfq
    rfq = next((r for r in rfqs if r['id'] == rfq_id), None)
    
    if rfq:
        with st.expander(f"📋 RFQ Details: #{rfq['id']:03d}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### RFQ Information")
                st.write(f"**RFQ ID:** #{rfq['id']:03d}")
                st.write(f"**Product/Service:** {rfq['product']}")
                st.write(f"**Customer:** {rfq['customer_name']}")
                st.write(f"**Description:** {rfq.get('description', 'N/A')}")
            
            with col2:
                st.markdown("#### Status & Timeline")
                st.write(f"**Status:** {rfq['status'].upper()}")
                st.write(f"**Received Date:** {rfq['received_date']}")
                st.write(f"**Notes:** {rfq.get('notes', 'No notes')}")
            
            # Actions
            st.markdown("#### Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📝 Create Estimation", width="stretch"):
                    st.switch_page("pages/04_💰_Estimations.py")
            
            with col2:
                if rfq['status'] == 'pending':
                    if st.button("✓ Approve RFQ", width="stretch"):
                        ds.update_rfq(rfq['id'], {'status': 'approved'})
                        st.success("RFQ approved successfully!")
                        st.rerun()
            
            with col3:
                if st.button("Close Details"):
                    st.session_state.selected_rfq = None
                    st.rerun()

# Footer
st.markdown("---")
st.caption("💡 Tip: Approve RFQs to create estimations and move forward with the project workflow.")

