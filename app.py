"""
Lab Management System (LMS) - Demo Application
Main entry point for the Streamlit application
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Paths
ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS_DIR / "techlink-logo.svg"

# Sidebar logo removed per request

# Import data initialization
from data.sample_data import initialize_data, reset_demo_data

# Page configuration
st.set_page_config(
    page_title="Lab Management System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #3b82f6;
        --secondary-color: #10b981;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    /* Success message */
    .success-message {
        padding: 1rem;
        background-color: #dcfce7;
        border-left: 4px solid #10b981;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Info box */
    .info-box {
        padding: 1rem;
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state and data
if 'initialized' not in st.session_state:
    initialize_data()
    st.session_state.initialized = True

# Sidebar utility: reload demo data
with st.sidebar:
    st.markdown("---")
    if st.button("🔄 Reload demo data", width="stretch"):
        reset_demo_data()
        st.success("Demo data reloaded")
        st.experimental_rerun()

# Main page content
def main():
    # Header with Techlink logo and title aligned on the same row
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=220)
    with col_title:
        st.markdown(
            """
<div class="main-header" style="margin:0;">
    <h1>🔬 Lab Management System</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        Comprehensive Lab Testing & Quality Management Solution
    </p>
</div>
""",
            unsafe_allow_html=True,
        )
    
    # Welcome section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Welcome to the LMS Demo")
        st.markdown("""
        This is a fully functional demonstration of our Lab Management System. 
        Explore the features using the sidebar navigation.
        
        **Key Features:**
        - 📊 Real-time Dashboard & Analytics
        - 👥 Customer & Project Management
        - 🧪 Complete Test Lifecycle Management
        - 📄 Document & Report Generation
        - 🔍 Quality Assurance & Compliance
        """)
        
        st.markdown("---")
        
        st.markdown("### Quick Start Guide")
        st.markdown("""
        1. **Dashboard** - View system overview and key metrics
        2. **Customers** - Manage client information
        3. **Projects** - Create and track projects
        4. **Test Plans** - Plan and schedule tests
        5. **Results** - Record and analyze test results
        """)
    
    with col2:
        st.markdown("### System Status")
        
        # Get current stats
        from services.data_service import DataService
        ds = DataService()
        
        st.metric("Active Projects", len([p for p in ds.get_all_projects() if p['status'] == 'active']))
        st.metric("Total Customers", len(ds.get_all_customers()))
        st.metric("Test Plans", len(ds.get_all_test_plans()))
        st.metric("Pending RFQs", len([r for r in ds.get_all_rfqs() if r['status'] == 'pending']))
        
        st.markdown("---")
        
        # Last updated
        st.markdown(f"""
        <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
            Last Updated<br/>
            {datetime.now().strftime("%B %d, %Y %H:%M")}
        </div>
        """, unsafe_allow_html=True)
    
    # Features overview
    st.markdown("---")
    st.markdown("### 📋 Available Modules")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Core Operations**
        - Dashboard
        - Customers
        - RFQs
        - Estimations
        - Projects
        """)
    
    with col2:
        st.markdown("""
        **Testing & QC**
        - Test Plans
        - Test Executions
        - Test Results
        - Samples
        - TRFs
        """)
    
    with col3:
        st.markdown("""
        **Registration & Compliance**
        - Lab Registration & Scope Management
        - Documents
        - Reports
        - Audits
        - NCRs
        - Certifications
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem;">
        <p>Lab Management System - Demo Version</p>
        <p>Built with Streamlit & Python | © 2024</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

