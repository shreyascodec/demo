"""
Estimations page - Cost estimation management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="Estimations", page_icon="💰", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("💰 Estimations")
st.markdown("Create and manage cost estimations for customer projects")

# Test type pricing
TEST_TYPES = {
    'EMC Testing': {'rate': 5000, 'hsn': '9030', 'duration': '5-7 days'},
    'RF Testing': {'rate': 6000, 'hsn': '9030', 'duration': '5-7 days'},
    'Safety Testing': {'rate': 4500, 'hsn': '9030', 'duration': '3-5 days'},
    'Environmental Testing': {'rate': 5500, 'hsn': '9030', 'duration': '4-6 days'},
    'Certification': {'rate': 7000, 'hsn': '9030', 'duration': '7-10 days'},
}

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Create Estimation", width="stretch"):
        st.session_state.show_add_estimation = True

# Add estimation form
if st.session_state.get('show_add_estimation', False):
    with st.form("add_estimation_form"):
        st.subheader("Create New Estimation")
        
        # Get RFQs and Customers
        rfqs = ds.get_all_rfqs()
        customers = ds.get_all_customers()
        
        rfq_options = {f"RFQ #{r['id']:03d} - {r['product']} ({r['customer_name']})": r for r in rfqs}
        
        col1, col2 = st.columns(2)
        
        with col1:
            if rfq_options:
                selected_rfq_str = st.selectbox("Select RFQ *", options=list(rfq_options.keys()))
                selected_rfq = rfq_options[selected_rfq_str]
                product = st.text_input("Product/Service *", value=selected_rfq['product'])
            else:
                st.warning("No RFQs available. Please create an RFQ first.")
                selected_rfq = None
                product = st.text_input("Product/Service *")
        
        with col2:
            status = st.selectbox("Status", ["draft", "sent", "approved", "rejected"])
            valid_days = st.number_input("Valid for (days)", min_value=1, max_value=90, value=30)
        
        st.markdown("### Select Test Types")
        st.markdown("Select the tests required and adjust quantities:")
        
        selected_tests = []
        total_cost = 0.0
        
        for test_type, details in TEST_TYPES.items():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                include = st.checkbox(test_type, key=f"test_{test_type}")
            
            with col2:
                st.write(f"₹{details['rate']:,}/unit")
            
            with col3:
                if include:
                    qty = st.number_input("Qty", min_value=1, max_value=10, value=1, key=f"qty_{test_type}")
                else:
                    qty = 1
                    st.write("-")
            
            with col4:
                if include:
                    cost = details['rate'] * qty
                    st.write(f"₹{cost:,}")
                    selected_tests.append(test_type)
                    total_cost += cost
                else:
                    st.write("-")
        
        st.markdown("---")
        st.markdown(f"### Total Estimated Cost: ₹{total_cost:,}")
        
        notes = st.text_area("Notes", placeholder="Any additional notes or terms...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Estimation", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if selected_rfq and product and selected_tests:
                valid_until = (datetime.now() + timedelta(days=valid_days)).strftime('%Y-%m-%d')
                
                new_estimation = {
                    'rfq_id': selected_rfq['id'],
                    'customer_id': selected_rfq['customer_id'],
                    'customer_name': selected_rfq['customer_name'],
                    'product': product,
                    'test_types': selected_tests,
                    'total_cost': total_cost,
                    'status': status,
                    'valid_until': valid_until,
                    'notes': notes,
                }
                ds.add_estimation(new_estimation)
                st.success(f"✅ Estimation created successfully! Total: ₹{total_cost:,}")
                st.session_state.show_add_estimation = False
                st.rerun()
            else:
                st.error("Please fill in all required fields and select at least one test type")
        
        if cancel:
            st.session_state.show_add_estimation = False
            st.rerun()

st.markdown("---")

# Statistics
estimations = ds.get_all_estimations()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Estimations", len(estimations))

with col2:
    draft_count = len([e for e in estimations if e['status'] == 'draft'])
    st.metric("Draft", draft_count)

with col3:
    approved_count = len([e for e in estimations if e['status'] == 'approved'])
    st.metric("Approved", approved_count)

with col4:
    total_value = sum([e['total_cost'] for e in estimations if e['status'] == 'approved'])
    st.metric("Approved Value", f"₹{total_value:,.0f}")

st.markdown("---")

# Display estimations
if estimations:
    st.subheader(f"Estimation List ({len(estimations)} results)")
    
    for est in estimations:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### EST-{est['id']:04d}")
                st.markdown(f"**Product:** {est['product']}")
                st.markdown(f"**Customer:** {est['customer_name']}")
                st.markdown(f"**Tests:** {', '.join(est['test_types'])}")
            
            with col2:
                st.markdown(f"**Total Cost:** ₹{est['total_cost']:,}")
                st.markdown(f"**Created:** {est['created_at']}")
                st.markdown(f"**Valid Until:** {est.get('valid_until', 'N/A')}")
            
            with col3:
                status = est['status']
                if status == 'draft':
                    st.info("DRAFT")
                elif status == 'sent':
                    st.warning("SENT")
                elif status == 'approved':
                    st.success("APPROVED")
                else:
                    st.error("REJECTED")
                
                if st.button("View Details", key=f"view_est_{est['id']}", width="stretch"):
                    st.session_state.selected_estimation = est['id']
                    st.rerun()
            
            st.markdown("---")
else:
    st.info("No estimations found. Create your first estimation from an RFQ!")

# Estimation details
if st.session_state.get('selected_estimation'):
    est_id = st.session_state.selected_estimation
    est = next((e for e in estimations if e['id'] == est_id), None)
    
    if est:
        with st.expander(f"💰 Estimation Details: EST-{est['id']:04d}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Estimation Information")
                st.write(f"**Estimation ID:** EST-{est['id']:04d}")
                st.write(f"**RFQ ID:** #{est['rfq_id']:03d}")
                st.write(f"**Customer:** {est['customer_name']}")
                st.write(f"**Product:** {est['product']}")
                st.write(f"**Status:** {est['status'].upper()}")
            
            with col2:
                st.markdown("#### Cost Details")
                st.write(f"**Total Cost:** ₹{est['total_cost']:,}")
                st.write(f"**Created:** {est['created_at']}")
                st.write(f"**Valid Until:** {est.get('valid_until', 'N/A')}")
                st.write(f"**Notes:** {est.get('notes', 'No notes')}")
            
            st.markdown("#### Test Types Included")
            for test_type in est['test_types']:
                details = TEST_TYPES.get(test_type, {})
                st.write(f"- **{test_type}** - ₹{details.get('rate', 0):,} ({details.get('duration', 'N/A')})")
            
            # Actions
            st.markdown("#### Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if est['status'] == 'approved':
                    if st.button("📁 Create Project", width="stretch"):
                        st.switch_page("pages/05_📁_Projects.py")
            
            with col2:
                if est['status'] == 'draft':
                    if st.button("📤 Mark as Sent", width="stretch"):
                        st.info("Marked as sent (update functionality)")
            
            with col3:
                if st.button("Close Details"):
                    st.session_state.selected_estimation = None
                    st.rerun()

# Test type reference
with st.expander("📚 Test Type Reference"):
    st.markdown("### Available Test Types and Rates")
    
    for test_type, details in TEST_TYPES.items():
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown(f"**{test_type}**")
        
        with col2:
            st.markdown(f"₹{details['rate']:,}/unit")
        
        with col3:
            st.markdown(f"Duration: {details['duration']}")

# Footer
st.markdown("---")
st.caption("💡 Tip: Create estimations from approved RFQs. Once approved, convert them to projects.")

