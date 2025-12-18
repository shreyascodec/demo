"""
Data service for managing all data operations
Uses session state for in-memory storage
"""

import streamlit as st
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

class DataService:
    """Central data service for all CRUD operations"""
    
    def __init__(self):
        """Initialize data service"""
        # Ensure session state is initialized
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state with demo data if not already done."""
        # If the main initializer hasn't run, populate all demo data now.
        if 'initialized' not in st.session_state:
            try:
                from data.sample_data import initialize_data
                initialize_data()
                return
            except Exception:
                # Fallback to empty structures if seeding fails
                pass

        if 'customers' not in st.session_state:
            st.session_state.customers = []
        if 'projects' not in st.session_state:
            st.session_state.projects = []
        if 'test_plans' not in st.session_state:
            st.session_state.test_plans = []
        if 'rfqs' not in st.session_state:
            st.session_state.rfqs = []
        if 'estimations' not in st.session_state:
            st.session_state.estimations = []
        if 'test_executions' not in st.session_state:
            st.session_state.test_executions = []
        if 'test_results' not in st.session_state:
            st.session_state.test_results = []
        if 'samples' not in st.session_state:
            st.session_state.samples = []
        if 'trfs' not in st.session_state:
            st.session_state.trfs = []
        if 'documents' not in st.session_state:
            st.session_state.documents = []
        if 'audits' not in st.session_state:
            st.session_state.audits = []
        if 'ncrs' not in st.session_state:
            st.session_state.ncrs = []
        if 'certifications' not in st.session_state:
            st.session_state.certifications = []
    
    # Customer operations
    def get_all_customers(self) -> List[Dict[str, Any]]:
        """Get all customers"""
        return st.session_state.customers
    
    def get_customer_by_id(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """Get customer by ID"""
        return next((c for c in st.session_state.customers if c['id'] == customer_id), None)
    
    def add_customer(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Add new customer"""
        customer['id'] = len(st.session_state.customers) + 1
        customer['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.customers.append(customer)
        return customer
    
    def update_customer(self, customer_id: int, updates: Dict[str, Any]) -> bool:
        """Update customer"""
        for i, customer in enumerate(st.session_state.customers):
            if customer['id'] == customer_id:
                st.session_state.customers[i].update(updates)
                return True
        return False
    
    def delete_customer(self, customer_id: int) -> bool:
        """Delete customer"""
        st.session_state.customers = [c for c in st.session_state.customers if c['id'] != customer_id]
        return True
    
    # Project operations
    def get_all_projects(self) -> List[Dict[str, Any]]:
        """Get all projects"""
        return st.session_state.projects
    
    def get_project_by_id(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get project by ID"""
        return next((p for p in st.session_state.projects if p['id'] == project_id), None)
    
    def add_project(self, project: Dict[str, Any]) -> Dict[str, Any]:
        """Add new project"""
        project['id'] = len(st.session_state.projects) + 1
        project['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.projects.append(project)
        return project
    
    def update_project(self, project_id: int, updates: Dict[str, Any]) -> bool:
        """Update project"""
        for i, project in enumerate(st.session_state.projects):
            if project['id'] == project_id:
                st.session_state.projects[i].update(updates)
                return True
        return False
    
    # Test Plan operations
    def get_all_test_plans(self) -> List[Dict[str, Any]]:
        """Get all test plans"""
        return st.session_state.test_plans
    
    def get_test_plans_by_project(self, project_id: int) -> List[Dict[str, Any]]:
        """Get test plans for a project"""
        return [tp for tp in st.session_state.test_plans if tp['project_id'] == project_id]
    
    def add_test_plan(self, test_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Add new test plan"""
        test_plan['id'] = len(st.session_state.test_plans) + 1
        test_plan['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.test_plans.append(test_plan)
        return test_plan
    
    def update_test_plan(self, test_plan_id: int, updates: Dict[str, Any]) -> bool:
        """Update test plan"""
        for i, tp in enumerate(st.session_state.test_plans):
            if tp['id'] == test_plan_id:
                st.session_state.test_plans[i].update(updates)
                return True
        return False
    
    # RFQ operations
    def get_all_rfqs(self) -> List[Dict[str, Any]]:
        """Get all RFQs"""
        return st.session_state.rfqs
    
    def add_rfq(self, rfq: Dict[str, Any]) -> Dict[str, Any]:
        """Add new RFQ"""
        rfq['id'] = len(st.session_state.rfqs) + 1
        rfq['received_date'] = datetime.now().strftime('%Y-%m-%d')
        st.session_state.rfqs.append(rfq)
        return rfq
    
    def update_rfq(self, rfq_id: int, updates: Dict[str, Any]) -> bool:
        """Update RFQ"""
        for i, rfq in enumerate(st.session_state.rfqs):
            if rfq['id'] == rfq_id:
                st.session_state.rfqs[i].update(updates)
                return True
        return False
    
    # Estimation operations
    def get_all_estimations(self) -> List[Dict[str, Any]]:
        """Get all estimations"""
        return st.session_state.estimations
    
    def add_estimation(self, estimation: Dict[str, Any]) -> Dict[str, Any]:
        """Add new estimation"""
        estimation['id'] = len(st.session_state.estimations) + 1
        estimation['created_at'] = datetime.now().strftime('%Y-%m-%d')
        st.session_state.estimations.append(estimation)
        return estimation
    
    # Test Execution operations
    def get_all_test_executions(self) -> List[Dict[str, Any]]:
        """Get all test executions"""
        return st.session_state.test_executions
    
    def get_test_executions_by_test_plan(self, test_plan_id: int) -> List[Dict[str, Any]]:
        """Get test executions for a test plan"""
        return [te for te in st.session_state.test_executions if te.get('test_plan_id') == test_plan_id]
    
    def add_test_execution(self, execution: Dict[str, Any]) -> Dict[str, Any]:
        """Add new test execution"""
        execution['id'] = len(st.session_state.test_executions) + 1
        execution['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.test_executions.append(execution)
        return execution
    
    # Test Result operations
    def get_all_test_results(self) -> List[Dict[str, Any]]:
        """Get all test results"""
        return st.session_state.test_results
    
    def get_test_results_by_test_plan(self, test_plan_id: int) -> List[Dict[str, Any]]:
        """Get test results for a test plan"""
        return [tr for tr in st.session_state.test_results if tr.get('test_plan_id') == test_plan_id]
    
    def add_test_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Add new test result"""
        result['id'] = len(st.session_state.test_results) + 1
        result['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.test_results.append(result)
        return result
    
    # Sample operations
    def get_all_samples(self) -> List[Dict[str, Any]]:
        """Get all samples"""
        return st.session_state.samples
    
    def add_sample(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Add new sample"""
        sample['id'] = len(st.session_state.samples) + 1
        sample['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.samples.append(sample)
        return sample
    
    # TRF operations
    def get_all_trfs(self) -> List[Dict[str, Any]]:
        """Get all TRFs"""
        return st.session_state.trfs
    
    def add_trf(self, trf: Dict[str, Any]) -> Dict[str, Any]:
        """Add new TRF"""
        trf['id'] = len(st.session_state.trfs) + 1
        trf['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.trfs.append(trf)
        return trf
    
    # Document operations
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents"""
        return st.session_state.documents
    
    def add_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Add new document"""
        document['id'] = len(st.session_state.documents) + 1
        document['uploaded_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.documents.append(document)
        return document
    
    # Audit operations
    def get_all_audits(self) -> List[Dict[str, Any]]:
        """Get all audits"""
        return st.session_state.audits
    
    def add_audit(self, audit: Dict[str, Any]) -> Dict[str, Any]:
        """Add new audit"""
        audit['id'] = len(st.session_state.audits) + 1
        audit['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.audits.append(audit)
        return audit
    
    # NCR operations
    def get_all_ncrs(self) -> List[Dict[str, Any]]:
        """Get all NCRs"""
        return st.session_state.ncrs
    
    def add_ncr(self, ncr: Dict[str, Any]) -> Dict[str, Any]:
        """Add new NCR"""
        ncr['id'] = len(st.session_state.ncrs) + 1
        ncr['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.ncrs.append(ncr)
        return ncr
    
    # Certification operations
    def get_all_certifications(self) -> List[Dict[str, Any]]:
        """Get all certifications"""
        return st.session_state.certifications
    
    def add_certification(self, certification: Dict[str, Any]) -> Dict[str, Any]:
        """Add new certification"""
        certification['id'] = len(st.session_state.certifications) + 1
        certification['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.certifications.append(certification)
        return certification
    
    # Statistics methods
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        projects = self.get_all_projects()
        test_plans = self.get_all_test_plans()
        
        return {
            'total_projects': len(projects),
            'active_projects': len([p for p in projects if p['status'] == 'active']),
            'completed_projects': len([p for p in projects if p['status'] == 'completed']),
            'total_customers': len(self.get_all_customers()),
            'total_test_plans': len(test_plans),
            'completed_tests': len([tp for tp in test_plans if tp['status'] == 'Completed']),
            'pending_rfqs': len([r for r in self.get_all_rfqs() if r['status'] == 'pending']),
            'total_samples': len(self.get_all_samples()),
        }

