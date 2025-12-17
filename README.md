# Lab Management System (LMS) - Demo

A fully functional demo of the Lab Management System built with Streamlit and Python.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the demo folder:**
```bash
cd demo
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
demo/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── pages/                 # Streamlit pages
│   ├── 01_📊_Dashboard.py
│   ├── 02_👥_Customers.py
│   ├── 03_📋_RFQs.py
│   ├── 04_💰_Estimations.py
│   ├── 05_📁_Projects.py
│   ├── 06_🔬_Samples.py
│   ├── 07_🧪_Test_Plans.py
│   ├── 08_⚗️_Test_Executions.py
│   ├── 09_📈_Test_Results.py
│   ├── 10_📄_TRFs.py
│   ├── 11_📚_Documents.py
│   ├── 12_📑_Reports.py
│   ├── 13_🔍_Audits.py
│   ├── 14_⚠️_NCRs.py
│   └── 15_🏆_Certifications.py
├── models/                # Data models
│   ├── __init__.py
│   ├── customer.py
│   ├── project.py
│   ├── test_plan.py
│   └── ...
├── services/              # Business logic
│   ├── __init__.py
│   ├── data_service.py
│   └── chart_service.py
└── data/                  # Sample data
    ├── __init__.py
    └── sample_data.py
```

## ✨ Features

### Core Modules

1. **Dashboard** - Real-time analytics and KPIs
   - Project statistics
   - Performance metrics
   - Activity timeline
   - Interactive charts

2. **Customer Management** - Client database
   - Add/Edit/View customers
   - Company details
   - Contact information

3. **RFQs** - Request for Quotation tracking
   - RFQ creation and management
   - Status tracking
   - Customer linking

4. **Estimations** - Cost estimation tool
   - Test type selection
   - Automatic cost calculation
   - HSN code management

5. **Projects** - Project management
   - Project creation and tracking
   - Status management
   - Client association
   - Test plan linking

6. **Test Plans** - Test planning module
   - Test plan creation
   - Engineer assignment
   - Test type specification
   - Status tracking

7. **Test Executions** - Test execution tracking
   - Execution logging
   - Progress monitoring
   - Result recording

8. **Test Results** - Result management
   - Pass/Fail recording
   - Data logging
   - Result analysis

9. **Samples** - Sample tracking
   - Sample registration
   - Barcode generation
   - Status tracking

10. **TRFs** - Test Request Forms
    - TRF creation
    - Approval workflow
    - Document management

11. **Documents** - Document repository
    - Upload/Download
    - Version control
    - Category management

12. **Reports** - Report generation
    - Test reports
    - Project reports
    - Custom reports

13. **Audits** - Audit management
    - Audit scheduling
    - Finding tracking
    - Compliance monitoring

14. **NCRs** - Non-Conformance Reports
    - NCR creation
    - Root cause analysis
    - Corrective action tracking

15. **Certifications** - Certification management
    - Certificate tracking
    - Expiry monitoring
    - Renewal alerts

## 🎨 UI Features

- **Modern Design** - Clean, professional interface
- **Interactive Charts** - Recharts-style visualizations using Plotly
- **Real-time Updates** - Dynamic data refresh
- **Responsive Layout** - Works on all screen sizes
- **Dark/Light Mode** - Theme support (Streamlit native)

## 📊 Sample Data

The demo includes pre-populated sample data:
- 4 Customers
- 2 RFQs
- 3 Estimations
- 5 Projects
- 8 Test Plans
- Various samples, TRFs, and other records

## 🔧 Customization

### Adding New Data
Data is stored in-memory using Python objects. To add persistent storage:
1. Uncomment SQLite code in `services/data_service.py`
2. Or implement your preferred database

### Modifying Sample Data
Edit `data/sample_data.py` to customize initial data

### Styling
Streamlit themes can be configured in `.streamlit/config.toml`

## 📝 Notes

- This is a demo version with in-memory data storage
- Data resets when the application restarts
- For production, integrate with your backend API
- All features are fully functional for demonstration purposes

## 🎯 Demo Tips

1. **Start with Dashboard** - Shows overview of all modules
2. **Create a Project** - Navigate to Projects page
3. **Add Test Plans** - Associate tests with projects
4. **Track Progress** - Use Test Executions page
5. **View Analytics** - Return to Dashboard for insights

## 🆘 Support

For issues or questions:
- Check the main LMS README
- Review the codebase documentation
- Contact the development team

## 📜 License

Part of the Lab Management System (LMS) project.

---

**Built with ❤️ using Streamlit and Python**

