"""
Estimations page - Cost estimation management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

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
        
        st.markdown("---")
        st.markdown("### Precompliance Testing")
        st.info("💡 Precompliance includes 3-4 tests in general. Costs are comparatively lower than compliance testing.")
        
        precompliance_col1, precompliance_col2, precompliance_col3, precompliance_col4 = st.columns(4)
        
        with precompliance_col1:
            precompliance_num_tests = st.number_input("Number of Tests", min_value=1, max_value=10, value=3, key="precompliance_tests", help="Typically 3-4 tests")
        
        with precompliance_col2:
            precompliance_cycle_cost = st.number_input("Cost per 8hr Cycle (₹)", min_value=0.0, value=15000.0, step=1000.0, key="precompliance_cycle_cost", format="%.2f")
        
        with precompliance_col3:
            precompliance_cycles = st.number_input("Number of Cycles", min_value=1, max_value=20, value=1, key="precompliance_cycles")
        
        with precompliance_col4:
            precompliance_total = precompliance_cycle_cost * precompliance_cycles
            st.metric("Precompliance Total", f"₹{precompliance_total:,.2f}")
        
        st.markdown("---")
        st.markdown("### Compliance Testing")
        st.warning("⚠️ Compliance considers 1 test depending upon product success. Many cycles may be required if tests fail.")
        
        compliance_col1, compliance_col2, compliance_col3, compliance_col4 = st.columns(4)
        
        with compliance_col1:
            compliance_num_tests = st.number_input("Number of Tests", min_value=1, max_value=10, value=1, key="compliance_tests", help="Typically 1 test per product")
        
        with compliance_col2:
            compliance_cycle_cost = st.number_input("Cost per 8hr Cycle (₹)", min_value=0.0, value=25000.0, step=1000.0, key="compliance_cycle_cost", format="%.2f", help="Higher than precompliance")
        
        with compliance_col3:
            compliance_cycles = st.number_input("Number of Cycles", min_value=1, max_value=50, value=1, key="compliance_cycles", help="May require multiple cycles if product fails")
        
        with compliance_col4:
            compliance_total = compliance_cycle_cost * compliance_cycles
            st.metric("Compliance Total", f"₹{compliance_total:,.2f}")
        
        st.markdown("---")
        
        # Calculate totals
        total_cost = precompliance_total + compliance_total
        
        # Display cost breakdown
        cost_col1, cost_col2 = st.columns(2)
        
        with cost_col1:
            st.markdown("#### Cost Breakdown")
            st.write(f"**Precompliance Cost:** ₹{precompliance_total:,.2f}")
            st.write(f"  - {precompliance_num_tests} test(s) × {precompliance_cycles} cycle(s) × ₹{precompliance_cycle_cost:,.2f}/cycle")
            st.write(f"**Compliance Cost:** ₹{compliance_total:,.2f}")
            st.write(f"  - {compliance_num_tests} test(s) × {compliance_cycles} cycle(s) × ₹{compliance_cycle_cost:,.2f}/cycle")
        
        with cost_col2:
            st.markdown("#### Summary")
            st.metric("Total Estimated Cost", f"₹{total_cost:,.2f}")
            if compliance_cycles > 1:
                st.info(f"⚠️ Note: {compliance_cycles} compliance cycles included. Additional cycles may be required if product fails.")
        
        # Store test types for backward compatibility
        selected_tests = []
        if precompliance_num_tests > 0:
            selected_tests.append(f"Precompliance ({precompliance_num_tests} tests)")
        if compliance_num_tests > 0:
            selected_tests.append(f"Compliance ({compliance_num_tests} test)")
        
        notes = st.text_area("Notes", placeholder="Any additional notes or terms...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Create Estimation", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if selected_rfq and product:
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
                    # Precompliance details
                    'precompliance': {
                        'num_tests': precompliance_num_tests,
                        'cycle_cost': precompliance_cycle_cost,
                        'num_cycles': precompliance_cycles,
                        'total_cost': precompliance_total,
                    },
                    # Compliance details
                    'compliance': {
                        'num_tests': compliance_num_tests,
                        'cycle_cost': compliance_cycle_cost,
                        'num_cycles': compliance_cycles,
                        'total_cost': compliance_total,
                    },
                }
                ds.add_estimation(new_estimation)
                st.success(f"✅ Estimation created successfully! Total: ₹{total_cost:,.2f}")
                st.session_state.show_add_estimation = False
                st.rerun()
            else:
                st.error("Please fill in all required fields")
        
        if cancel:
            st.session_state.show_add_estimation = False
            st.rerun()

st.markdown("---")

# Statistics
estimations = ds.get_all_estimations()

col1, col2, col3, col4, col5, col6 = st.columns(6)

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

with col5:
    # Calculate precompliance total
    precompliance_total = sum([
        e.get('precompliance', {}).get('total_cost', 0) 
        for e in estimations 
        if e.get('precompliance')
    ])
    st.metric("Precompliance Total", f"₹{precompliance_total:,.0f}")

with col6:
    # Calculate compliance total
    compliance_total = sum([
        e.get('compliance', {}).get('total_cost', 0) 
        for e in estimations 
        if e.get('compliance')
    ])
    st.metric("Compliance Total", f"₹{compliance_total:,.0f}")

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
                
                # Show precompliance and compliance costs if available
                if est.get('precompliance') and est.get('compliance'):
                    precompliance = est['precompliance']
                    compliance = est['compliance']
                    st.markdown(f"**Precompliance:** ₹{precompliance.get('total_cost', 0):,.2f} | **Compliance:** ₹{compliance.get('total_cost', 0):,.2f}")
                else:
                    st.markdown(f"**Tests:** {', '.join(est.get('test_types', []))}")
            
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
            
            # Display Precompliance and Compliance breakdown
            if est.get('precompliance') and est.get('compliance'):
                st.markdown("---")
                st.markdown("#### Precompliance Testing")
                precompliance = est['precompliance']
                precompliance_col1, precompliance_col2, precompliance_col3 = st.columns(3)
                
                with precompliance_col1:
                    st.write(f"**Number of Tests:** {precompliance.get('num_tests', 0)}")
                    st.caption("Typically 3-4 tests in general")
                
                with precompliance_col2:
                    st.write(f"**Cost per 8hr Cycle:** ₹{precompliance.get('cycle_cost', 0):,.2f}")
                    st.write(f"**Number of Cycles:** {precompliance.get('num_cycles', 0)}")
                
                with precompliance_col3:
                    st.metric("Precompliance Total", f"₹{precompliance.get('total_cost', 0):,.2f}")
                    st.caption("Costs are lower than compliance")
                
                st.markdown("---")
                st.markdown("#### Compliance Testing")
                compliance = est['compliance']
                compliance_col1, compliance_col2, compliance_col3 = st.columns(3)
                
                with compliance_col1:
                    st.write(f"**Number of Tests:** {compliance.get('num_tests', 0)}")
                    st.caption("1 test depending upon product success")
                
                with compliance_col2:
                    st.write(f"**Cost per 8hr Cycle:** ₹{compliance.get('cycle_cost', 0):,.2f}")
                    st.write(f"**Number of Cycles:** {compliance.get('num_cycles', 0)}")
                    if compliance.get('num_cycles', 0) > 1:
                        st.warning("⚠️ Multiple cycles may indicate product failures")
                
                with compliance_col3:
                    st.metric("Compliance Total", f"₹{compliance.get('total_cost', 0):,.2f}")
                    st.caption("Higher cost than precompliance")
                
                st.markdown("---")
                st.markdown("#### Cost Summary")
                summary_col1, summary_col2 = st.columns(2)
                
                with summary_col1:
                    st.write(f"**Precompliance:** ₹{precompliance.get('total_cost', 0):,.2f}")
                    st.write(f"**Compliance:** ₹{compliance.get('total_cost', 0):,.2f}")
                
                with summary_col2:
                    st.metric("Grand Total", f"₹{est['total_cost']:,.2f}")
            else:
                # Fallback for old format
                st.markdown("#### Test Types Included")
                for test_type in est.get('test_types', []):
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

# Rate chart reference
with st.expander("📚 Rate Chart & Pricing Reference", expanded=False):
    st.markdown("### Testing Categories & 8hr Cycle Pricing")
    
    st.markdown("---")
    st.markdown("#### 🔬 Precompliance Testing")
    
    precompliance_info_col1, precompliance_info_col2 = st.columns(2)
    
    with precompliance_info_col1:
        st.markdown("**Characteristics:**")
        st.write("• Typically includes **3-4 tests** in general")
        st.write("• Costs are **comparatively lower** than compliance testing")
        st.write("• Used for initial product validation")
        st.write("• Helps identify issues before formal compliance testing")
    
    with precompliance_info_col2:
        st.markdown("**Pricing Structure:**")
        st.write("• **Cost per 8hr Cycle:** ₹15,000 - ₹20,000")
        st.write("• **Typical Cycles:** 1-2 cycles")
        st.write("• **Total Range:** ₹15,000 - ₹40,000")
        st.write("• **Example:** 3 tests × 1 cycle × ₹15,000 = ₹15,000")
    
    st.markdown("---")
    st.markdown("#### ✅ Compliance Testing")
    
    compliance_info_col1, compliance_info_col2 = st.columns(2)
    
    with compliance_info_col1:
        st.markdown("**Characteristics:**")
        st.write("• Typically **1 test** depending upon product success")
        st.write("• Costs are **higher** than precompliance")
        st.write("• Required for formal certification")
        st.write("• **Many cycles may be required if product fails**")
    
    with compliance_info_col2:
        st.markdown("**Pricing Structure:**")
        st.write("• **Cost per 8hr Cycle:** ₹25,000 - ₹30,000")
        st.write("• **Typical Cycles:** 1 cycle (if successful)")
        st.write("• **Failed Products:** 2-5+ cycles may be required")
        st.write("• **Total Range:** ₹25,000 - ₹150,000+")
        st.write("• **Example:** 1 test × 2 cycles × ₹25,000 = ₹50,000")
    
    st.markdown("---")
    st.markdown("#### 💰 Cost Comparison")
    
    comparison_data = {
        "Category": ["Precompliance", "Compliance"],
        "Tests (Typical)": ["3-4 tests", "1 test"],
        "Cost per 8hr Cycle": ["₹15,000 - ₹20,000", "₹25,000 - ₹30,000"],
        "Typical Cycles": ["1-2 cycles", "1 cycle (success) / 2-5+ (failure)"],
        "Total Cost Range": ["₹15,000 - ₹40,000", "₹25,000 - ₹150,000+"]
    }
    
    # Display as a table
    df = pd.DataFrame(comparison_data)
    st.table(df)
    
    st.markdown("---")
    st.markdown("#### 📊 Pricing Examples")
    
    example_col1, example_col2 = st.columns(2)
    
    with example_col1:
        st.markdown("**Example 1: Standard Package**")
        st.write("• Precompliance: 3 tests × 1 cycle × ₹15,000 = **₹15,000**")
        st.write("• Compliance: 1 test × 1 cycle × ₹25,000 = **₹25,000**")
        st.write("• **Total: ₹40,000**")
    
    with example_col2:
        st.markdown("**Example 2: Product with Failures**")
        st.write("• Precompliance: 4 tests × 2 cycles × ₹15,000 = **₹30,000**")
        st.write("• Compliance: 1 test × 3 cycles × ₹27,500 = **₹82,500**")
        st.write("• **Total: ₹112,500**")
    
    st.markdown("---")
    st.markdown("#### ℹ️ Important Notes")
    st.info("""
    **Key Points:**
    - All costs are based on **8-hour testing cycles**
    - Precompliance testing helps reduce compliance failures
    - Compliance testing costs increase significantly with multiple cycles
    - Actual costs may vary based on product complexity and test requirements
    - Additional cycles may be required if products fail initial compliance testing
    """)
    
    st.markdown("---")
    st.markdown("#### 📋 Legacy Test Types (Reference)")
    st.caption("Note: These are legacy test types. New estimations use Precompliance/Compliance structure.")
    
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

