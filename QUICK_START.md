# 🚀 Quick Start - 3 Simple Steps

## Ready to run your LMS demo in 3 minutes!

### Step 1️⃣: Open PowerShell in this folder
Right-click in the `demo` folder and select "Open in Terminal" or "Open PowerShell window here"

### Step 2️⃣: Run the startup script
```powershell
.\start_demo.ps1
```

**OR** if you prefer manual commands:

```powershell
pip install -r requirements.txt
streamlit run app.py
```

### Step 3️⃣: Done! ✅
The app will open automatically in your browser at `http://localhost:8501`

---

## 🎯 Quick Demo Path

Follow this 5-minute demo sequence:

1. **📊 Dashboard** → View overview
2. **👥 Customers** → Add new customer: "Demo Corp"
3. **📋 RFQs** → Create RFQ for Demo Corp
4. **💰 Estimations** → Generate estimation
5. **📁 Projects** → Create project
6. **🧪 Test Plans** → Add test plan
7. **📊 Dashboard** → See updated metrics!

---

## ⚡ Troubleshooting

**Problem:** Script won't run
**Solution:** 
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\start_demo.ps1
```

**Problem:** Dependencies fail to install
**Solution:**
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Problem:** Port already in use
**Solution:**
```powershell
streamlit run app.py --server.port 8502
```

---

## 📖 Need More Info?

- **Detailed Setup:** See `SETUP_GUIDE.md`
- **Presentation Tips:** See `PRESENTATION_GUIDE.md`
- **Features:** See `README.md`

---

**🎉 Ready for your townhall demo!**

