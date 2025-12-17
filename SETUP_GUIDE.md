# LMS Demo Setup Guide

## Quick Start (5 minutes)

### Step 1: Open Terminal
Navigate to the demo folder:
```bash
cd demo
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- Pandas (data manipulation)
- Plotly (interactive charts)
- NumPy (numerical computing)

### Step 3: Run the Application
```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## Troubleshooting

### Issue: "Command 'streamlit' not found"
**Solution:** Make sure pip installation completed successfully. Try:
```bash
python -m pip install streamlit
python -m streamlit run app.py
```

### Issue: "Port 8501 already in use"
**Solution:** Kill the existing process or use a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue: "Module not found" errors
**Solution:** Reinstall requirements:
```bash
pip install -r requirements.txt --upgrade
```

## Demo Features Checklist

After launching, verify these features work:

### ✅ Core Features
- [x] Dashboard with KPIs and charts
- [x] Customer management (Add/View/Search)
- [x] RFQ creation and approval
- [x] Cost estimation with test types
- [x] Project creation and tracking
- [x] Test plan management
- [x] Test execution tracking
- [x] Test results visualization

### ✅ Additional Features
- [x] Sample registration and tracking
- [x] TRF (Test Request Form) management
- [x] Document upload and categorization
- [x] Report generation and export
- [x] Audit scheduling and tracking
- [x] NCR (Non-Conformance) management
- [x] Certification tracking with expiry alerts

## Demo Data

The application comes pre-populated with sample data:
- 4 Customers
- 3 RFQs
- 3 Estimations
- 5 Projects
- 8 Test Plans
- Various related records

## Navigation Tips

1. **Use the sidebar** to switch between modules
2. **Search bars** are available on most pages
3. **Filter options** help narrow down results
4. **Action buttons** (➕) are in the top-right of each page
5. **Details buttons** show more information

## Customization

### Change Theme Colors
Edit `demo/.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#your-color"
```

### Modify Sample Data
Edit `demo/data/sample_data.py`

### Add New Test Types
Edit pricing in `demo/pages/04_💰_Estimations.py`

## Browser Compatibility

Tested on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

## Performance Tips

1. **For large datasets:** Consider implementing database pagination
2. **For slow charts:** Reduce data points or use sampling
3. **For memory issues:** Restart the Streamlit server

## Demo Workflow

Follow this workflow to demonstrate all features:

### 1. Dashboard (Start Here)
- Show overview metrics
- Explain KPIs
- Demonstrate charts

### 2. Customer Management
- Add a new customer
- Search for customers
- View customer details

### 3. RFQ → Estimation → Project
- Create an RFQ for the new customer
- Approve the RFQ
- Create an estimation from the RFQ
- Generate a project from the estimation

### 4. Test Planning & Execution
- Create a test plan for the project
- Start the test execution
- Record test results

### 5. Documentation & Compliance
- Upload documents
- Generate reports
- Schedule audits
- Track certifications

## Keyboard Shortcuts

- `Ctrl + R` - Refresh page
- `Ctrl + S` - Save (forms)
- `Esc` - Close modals/forms

## Support

For issues or questions:
1. Check this guide first
2. Review the main README.md
3. Check Streamlit documentation: https://docs.streamlit.io
4. Contact the development team

## Next Steps

After the demo, consider:
1. Integrating with your backend API
2. Implementing database persistence
3. Adding user authentication
4. Customizing for your specific workflows
5. Deploying to production

---

**Ready for your townhall demo! 🎉**

