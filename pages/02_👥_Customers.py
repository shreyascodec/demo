"""
Customers page - Manage customer/client information
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="Customers", page_icon="👥", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("👥 Customers")
st.markdown("Manage your customer and client information")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Add New Customer", width="stretch"):
        st.session_state.show_add_customer = True

# Add customer form
if st.session_state.get('show_add_customer', False):
    with st.form("add_customer_form"):
        st.subheader("Add New Customer")
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name *", placeholder="Enter company name")
            email = st.text_input("Email *", placeholder="contact@company.com")
            contact_person = st.text_input("Contact Person", placeholder="John Doe")
        
        with col2:
            phone = st.text_input("Phone", placeholder="+91 9876543210")
            gst_number = st.text_input("GST Number", placeholder="29AABCT1234F1Z5")
            status = st.selectbox("Status", ["active", "inactive"])
        
        address = st.text_area("Address", placeholder="Complete address with pincode")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Add Customer", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if company_name and email:
                new_customer = {
                    'company_name': company_name,
                    'email': email,
                    'contact_person': contact_person,
                    'phone': phone,
                    'address': address,
                    'gst_number': gst_number,
                    'status': status,
                }
                ds.add_customer(new_customer)
                st.success(f"✅ Customer '{company_name}' added successfully!")
                st.session_state.show_add_customer = False
                st.rerun()
            else:
                st.error("Please fill in all required fields (marked with *)")
        
        if cancel:
            st.session_state.show_add_customer = False
            st.rerun()

st.markdown("---")

# Search and filter
col1, col2 = st.columns([3, 1])

with col1:
    search_term = st.text_input("🔍 Search customers", placeholder="Search by company name, email, or contact person...")

with col2:
    status_filter = st.selectbox("Filter by Status", ["All", "active", "inactive"])

# Get customers
customers = ds.get_all_customers()

# Apply filters
if search_term:
    customers = [c for c in customers if 
                 search_term.lower() in c.get('company_name', '').lower() or
                 search_term.lower() in c.get('email', '').lower() or
                 search_term.lower() in c.get('contact_person', '').lower()]

if status_filter != "All":
    customers = [c for c in customers if c.get('status') == status_filter]

# Display statistics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", len(ds.get_all_customers()))

with col2:
    active_customers = len([c for c in ds.get_all_customers() if c.get('status') == 'active'])
    st.metric("Active Customers", active_customers)

with col3:
    # Count projects per customer
    projects = ds.get_all_projects()
    clients_with_projects = len(set([p['client_id'] for p in projects]))
    st.metric("Clients with Projects", clients_with_projects)

with col4:
    st.metric("Filtered Results", len(customers))

st.markdown("---")

# Display customers
if customers:
    st.subheader(f"Customer List ({len(customers)} results)")
    
    # Create cards for each customer
    for customer in customers:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### {customer['company_name']}")
                st.markdown(f"**Contact:** {customer.get('contact_person', 'N/A')}")
                st.markdown(f"**Email:** {customer.get('email', 'N/A')}")
                st.markdown(f"**Phone:** {customer.get('phone', 'N/A')}")
            
            with col2:
                st.markdown(f"**GST:** {customer.get('gst_number', 'N/A')}")
                st.markdown(f"**Address:** {customer.get('address', 'N/A')}")
                st.markdown(f"**Created:** {customer.get('created_at', 'N/A')}")
            
            with col3:
                status = customer.get('status', 'active')
                if status == 'active':
                    st.success("ACTIVE")
                else:
                    st.warning("INACTIVE")
                
                # Count customer's projects
                customer_projects = [p for p in ds.get_all_projects() if p['client_id'] == customer['id']]
                st.info(f"**{len(customer_projects)}** Projects")
                
                if st.button("View Details", key=f"view_{customer['id']}", width="stretch"):
                    st.session_state.selected_customer = customer['id']
                    st.info(f"Customer ID: {customer['id']} - Details view coming soon!")
            
            st.markdown("---")
else:
    st.info("No customers found. Add your first customer to get started!")

# Customer details in expander (if selected)
if st.session_state.get('selected_customer'):
    customer_id = st.session_state.selected_customer
    customer = ds.get_customer_by_id(customer_id)
    
    if customer:
        with st.expander(f"📋 Details: {customer['company_name']}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Company Information")
                st.write(f"**ID:** {customer['id']}")
                st.write(f"**Company:** {customer['company_name']}")
                st.write(f"**Email:** {customer['email']}")
                st.write(f"**Phone:** {customer.get('phone', 'N/A')}")
                st.write(f"**Contact Person:** {customer.get('contact_person', 'N/A')}")
            
            with col2:
                st.markdown("#### Additional Details")
                st.write(f"**GST Number:** {customer.get('gst_number', 'N/A')}")
                st.write(f"**Address:** {customer.get('address', 'N/A')}")
                st.write(f"**Status:** {customer.get('status', 'active').upper()}")
                st.write(f"**Created:** {customer.get('created_at', 'N/A')}")
            
            # Show related projects
            st.markdown("#### Related Projects")
            customer_projects = [p for p in ds.get_all_projects() if p['client_id'] == customer_id]
            
            if customer_projects:
                for proj in customer_projects:
                    st.markdown(f"- **{proj['name']}** ({proj['code']}) - Status: {proj['status']}")
            else:
                st.info("No projects found for this customer")
            
            if st.button("Close Details"):
                st.session_state.selected_customer = None
                st.rerun()

# Footer
st.markdown("---")
st.caption("💡 Tip: Use the search box to quickly find customers. Click 'Add New Customer' to register a new client.")

