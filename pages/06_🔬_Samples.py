"""
Samples page - Sample tracking and management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import random

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="Samples", page_icon="🔬", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("🔬 Samples")
st.markdown("Track and manage test samples")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Register Sample", width="stretch"):
        st.session_state.show_add_sample = True

# Add sample form
if st.session_state.get('show_add_sample', False):
    with st.form("add_sample_form"):
        st.subheader("Register New Sample")
        
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
            
            sample_name = st.text_input("Sample Name *", placeholder="Enter sample name")
            sample_type = st.selectbox("Sample Type", ["Product", "Component", "Material", "Other"])
        
        with col2:
            sample_number = st.text_input("Sample Number", placeholder="Auto-generated if empty")
            quantity = st.number_input("Quantity", min_value=1, value=1)
            status = st.selectbox("Status", ["received", "in_testing", "tested", "returned"])
        
        received_date = st.date_input("Received Date", value=datetime.now())
        description = st.text_area("Description", placeholder="Sample description and notes...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Register Sample", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if selected_project and sample_name:
                # Generate sample number if not provided
                if not sample_number:
                    sample_number = f"SMP-{random.randint(1000, 9999)}"
                
                new_sample = {
                    'project_id': selected_project['id'],
                    'project_name': selected_project['name'],
                    'sample_number': sample_number,
                    'name': sample_name,
                    'sample_type': sample_type,
                    'quantity': quantity,
                    'status': status,
                    'received_date': received_date.strftime('%Y-%m-%d'),
                    'description': description,
                }
                ds.add_sample(new_sample)
                st.success(f"✅ Sample '{sample_name}' registered successfully!")
                st.session_state.show_add_sample = False
                st.rerun()
            else:
                st.error("Please fill in all required fields")
        
        if cancel:
            st.session_state.show_add_sample = False
            st.rerun()

st.markdown("---")

# Statistics
samples = ds.get_all_samples()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Samples", len(samples))

with col2:
    in_testing = len([s for s in samples if s.get('status') == 'in_testing'])
    st.metric("In Testing", in_testing)

with col3:
    tested = len([s for s in samples if s.get('status') == 'tested'])
    st.metric("Tested", tested)

with col4:
    received = len([s for s in samples if s.get('status') == 'received'])
    st.metric("Received", received)

st.markdown("---")

# Display samples
if samples:
    st.subheader(f"Sample List ({len(samples)} samples)")
    
    for sample in samples:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### {sample['name']}")
                st.markdown(f"**Sample Number:** {sample.get('sample_number', 'N/A')}")
                st.markdown(f"**Project:** {sample.get('project_name', 'N/A')}")
                st.markdown(f"**Type:** {sample.get('sample_type', 'N/A')}")
            
            with col2:
                st.markdown(f"**Quantity:** {sample.get('quantity', 1)}")
                st.markdown(f"**Received:** {sample.get('received_date', 'N/A')}")
                if sample.get('description'):
                    st.markdown(f"*{sample['description'][:60]}...*" if len(sample.get('description', '')) > 60 else f"*{sample.get('description')}*")
            
            with col3:
                status = sample.get('status', 'received')
                if status == 'received':
                    st.info("RECEIVED")
                elif status == 'in_testing':
                    st.warning("IN TESTING")
                elif status == 'tested':
                    st.success("TESTED")
                else:
                    st.secondary("RETURNED")
                
                if st.button("View", key=f"view_sample_{sample['id']}", width="stretch"):
                    st.info(f"Sample details for {sample['sample_number']}")
            
            st.markdown("---")
else:
    st.info("No samples registered. Register your first sample to get started!")

# Footer
st.markdown("---")
st.caption("💡 Tip: Register samples when they arrive and update their status as testing progresses.")
