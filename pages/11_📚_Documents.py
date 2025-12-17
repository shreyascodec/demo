"""
Documents page - Document management
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService

st.set_page_config(page_title="Documents", page_icon="📚", layout="wide")

# Initialize services
ds = DataService()

# Header
st.title("📚 Documents")
st.markdown("Manage all project and test documents")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col3:
    if st.button("➕ Upload Document", width="stretch"):
        st.session_state.show_upload_doc = True

# Upload document form
if st.session_state.get('show_upload_doc', False):
    with st.form("upload_doc_form"):
        st.subheader("Upload New Document")
        
        col1, col2 = st.columns(2)
        
        with col1:
            doc_name = st.text_input("Document Name *", placeholder="Enter document name")
            category = st.selectbox("Category", [
                "Test Report", "Certificate", "Specification", 
                "Manual", "Drawing", "Other"
            ])
        
        with col2:
            version = st.text_input("Version", placeholder="v1.0")
            status = st.selectbox("Status", ["draft", "approved", "archived"])
        
        file_upload = st.file_uploader("Upload File", type=["pdf", "doc", "docx", "xlsx", "png", "jpg"])
        description = st.text_area("Description", placeholder="Document description...")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Upload Document", width="stretch")
        with col2:
            cancel = st.form_submit_button("Cancel", width="stretch")
        
        if submit:
            if doc_name:
                new_doc = {
                    'name': doc_name,
                    'category': category,
                    'version': version,
                    'status': status,
                    'description': description,
                    'filename': file_upload.name if file_upload else 'N/A',
                }
                ds.add_document(new_doc)
                st.success(f"✅ Document '{doc_name}' uploaded successfully!")
                st.session_state.show_upload_doc = False
                st.rerun()
            else:
                st.error("Please provide a document name")
        
        if cancel:
            st.session_state.show_upload_doc = False
            st.rerun()

st.markdown("---")

# Statistics
documents = ds.get_all_documents()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Documents", len(documents))

with col2:
    reports = len([d for d in documents if d.get('category') == 'Test Report'])
    st.metric("Test Reports", reports)

with col3:
    certificates = len([d for d in documents if d.get('category') == 'Certificate'])
    st.metric("Certificates", certificates)

with col4:
    approved = len([d for d in documents if d.get('status') == 'approved'])
    st.metric("Approved", approved)

st.markdown("---")

# Display documents
if documents:
    st.subheader(f"Document Library ({len(documents)} documents)")
    
    # Filters
    categories = sorted(list(set([d.get('category', 'Other') for d in documents])))
    selected_category = st.selectbox("Filter by Category", ["All"] + categories)
    selected_status = st.selectbox("Filter by Status", ["All", "draft", "approved", "archived"])
    search_term = st.text_input("Search", placeholder="Search by name or description...")
    
    filtered_docs = documents
    if selected_category != "All":
        filtered_docs = [d for d in filtered_docs if d.get('category') == selected_category]
    if selected_status != "All":
        filtered_docs = [d for d in filtered_docs if d.get('status') == selected_status]
    if search_term:
        s = search_term.lower()
        filtered_docs = [
            d for d in filtered_docs
            if s in d.get('name', '').lower() or s in d.get('description', '').lower()
        ]
    
    for doc in filtered_docs:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### 📄 {doc['name']}")
                st.markdown(f"**Category:** {doc.get('category', 'N/A')}")
                if doc.get('description'):
                    st.markdown(f"*{doc['description'][:80]}...*" if len(doc.get('description', '')) > 80 else f"*{doc.get('description')}*")
            
            with col2:
                st.markdown(f"**Version:** {doc.get('version', 'N/A')}")
                st.markdown(f"**Uploaded:** {doc.get('uploaded_at', 'N/A')}")
                st.markdown(f"**File:** {doc.get('filename', 'N/A')}")
            
            with col3:
                status = doc.get('status', 'draft')
                if status == 'approved':
                    st.success("APPROVED")
                elif status == 'draft':
                    st.info("DRAFT")
                else:
                    st.warning("ARCHIVED")
                
                if st.button("Download", key=f"download_{doc['id']}", width="stretch"):
                    st.info(f"Downloading {doc['name']}")
            
            st.markdown("---")
else:
    st.info("No documents uploaded yet. Upload your first document to get started!")

# Footer
st.markdown("---")
st.caption("💡 Tip: Upload test reports, certificates, and other important documents for easy access.")

