"""
Test Results page - View and manage test results
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from services.data_service import DataService
from services.chart_service import ChartService

st.set_page_config(page_title="Test Results", page_icon="📈", layout="wide")

# Initialize services
ds = DataService()
cs = ChartService()

# Header
st.title("📈 Test Results")
st.markdown("View and analyze test results")

# Statistics
test_results = ds.get_all_test_results()
test_executions = ds.get_all_test_executions() if hasattr(ds, "get_all_test_executions") else []

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Results", len(test_results))

with col2:
    passed = len([tr for tr in test_results if tr.get('pass_fail') == 'Pass'])
    st.metric("Passed", passed)

with col3:
    failed = len([tr for tr in test_results if tr.get('pass_fail') == 'Fail'])
    st.metric("Failed", failed)

with col4:
    if len(test_results) > 0:
        pass_rate = (passed / len(test_results)) * 100
    else:
        pass_rate = 0
    st.metric("Pass Rate", f"{pass_rate:.1f}%")

st.markdown("---")

# Results visualization
if test_results:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pass/Fail Distribution")
        result_data = [
            {'result': 'Pass', 'count': passed},
            {'result': 'Fail', 'count': failed}
        ]
        if sum(r['count'] for r in result_data) > 0:
            fig = cs.create_pie_chart(result_data, 'count', 'result', 'Test Results')
            st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.subheader("Results by Test Type")
        type_results = {}
        for tr in test_results:
            test_type = tr.get('test_type', 'Unknown')
            if test_type not in type_results:
                type_results[test_type] = {'passed': 0, 'failed': 0}
            if tr.get('pass_fail') == 'Pass':
                type_results[test_type]['passed'] += 1
            else:
                type_results[test_type]['failed'] += 1
        
        if type_results:
            type_data = [{'type': k, 'passed': v['passed'], 'failed': v['failed']} 
                        for k, v in type_results.items()]
            fig = cs.create_stacked_bar_chart(type_data, 'type', ['passed', 'failed'], 
                                             'Results by Test Type')
            st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # Results table
    st.subheader("Recent Test Results")
    for result in test_results[:10]:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**Result #{result['id']}**")
                st.markdown(f"Test: {result.get('test_name', 'N/A')}")
            
            with col2:
                st.markdown(f"Type: {result.get('test_type', 'N/A')}")
                st.markdown(f"Date: {result.get('created_at', 'N/A')}")
            
            with col3:
                if result.get('pass_fail') == 'Pass':
                    st.success("PASS")
                else:
                    st.error("FAIL")
            
            st.markdown("---")
else:
    st.info("No test results available. Execute tests and record results to see them here.")

# Footer
st.markdown("---")
st.caption("💡 Tip: Test results are automatically recorded when test executions are completed.")

# Recent executions (if any)
if test_executions:
    st.subheader("Recent Test Executions")
    for execn in test_executions[:5]:
        with st.container():
            col1, col2, col3 = st.columns([3,2,1])
            with col1:
                st.markdown(f"**{execn.get('test_name','Execution')}**")
                st.markdown(f"Project: {execn.get('project_name','N/A')}")
            with col2:
                st.markdown(f"Start: {execn.get('started_at','N/A')}")
                st.markdown(f"End: {execn.get('ended_at','N/A')}")
            with col3:
                res = execn.get('result','N/A')
                if res == 'Pass':
                    st.success("PASS")
                elif res == 'Fail':
                    st.error("FAIL")
                else:
                    st.info(res)
        st.markdown("---")
