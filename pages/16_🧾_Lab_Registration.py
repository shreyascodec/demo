"""
Lab Registration & Scope Management
----------------------------------
Interactive wizard that mirrors the LMS registration flow:
- Organization Details
- Scope Management
- Manpower
- Checklist & Payment Readiness

Data is stored in Streamlit session state for this demo.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

import streamlit as st

# Ensure project root is on path (for future integrations if needed)
sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(page_title="Lab Registration", page_icon="📄", layout="wide")


# -------- Session-State Helpers -------- #

def _init_lab_registration_state() -> None:
    """Initialize lab registration data in session state if missing."""
    if "lab_registration" not in st.session_state:
        st.session_state.lab_registration = {
            "organization": {
                "lab_name": "",
                "legal_name": "",
                "address": "",
                "city": "",
                "state": "",
                "country": "India",
                "contact_person": "",
                "email": "",
                "phone": "",
                "type_of_org": "",
                "parent_org": "",
                "working_days": "",
                "working_hours": "",
                "bank_name": "",
                "account_number": "",
                "ifsc": "",
                "has_statutory_docs": False,
                "has_accreditation_docs": False,
                "has_other_details": False,
            },
            "scope": {
                "scopes": [],  # list of dicts
                "equipments": [],  # list of dicts
            },
            "manpower": {
                "personnel": [],  # list of dicts
            },
        }

    if "lab_registration_current_step" not in st.session_state:
        st.session_state.lab_registration_current_step = "Organization Details"


def _get_lab_registration() -> Dict[str, Any]:
    return st.session_state.lab_registration


def _compute_step_statuses(reg: Dict[str, Any]) -> Dict[str, bool]:
    """Determine which steps are completed based on minimal required data."""
    org = reg["organization"]
    scope = reg["scope"]
    manpower = reg["manpower"]

    org_required = [
        "lab_name",
        "address",
        "contact_person",
        "email",
        "type_of_org",
        "working_days",
    ]
    org_completed = all(bool(org.get(f)) for f in org_required)

    scope_completed = bool(scope["scopes"] and scope["equipments"])

    manpower_completed = any(
        p.get("first_name")
        and p.get("last_name")
        and p.get("email")
        and p.get("mobile")
        and p.get("designation")
        for p in manpower["personnel"]
    )

    checklist_completed = org_completed and scope_completed and manpower_completed

    return {
        "Organization Details": org_completed,
        "Scope Management": scope_completed,
        "Manpower": manpower_completed,
        "Checklist": checklist_completed,
    }


# -------- UI Sections -------- #

def _render_step_header(step_labels: List[str], statuses: Dict[str, bool]) -> str:
    """Render step selector and status badges, return current step label."""
    st.title("Lab Registration & Scope Management")
    st.markdown(
        "This wizard mirrors the LMS registration flow (Organization Details, Scope Management, Manpower, Checklist) in a simplified way for demo purposes."
    )

    current_step = st.radio(
        "Registration steps",
        step_labels,
        index=step_labels.index(st.session_state.lab_registration_current_step),
        horizontal=True,
    )
    st.session_state.lab_registration_current_step = current_step

    status_cols = st.columns(len(step_labels))
    for idx, label in enumerate(step_labels):
        with status_cols[idx]:
            if statuses[label]:
                st.markdown(f"**{label}**\\nCompleted")
            else:
                st.markdown(f"**{label}**\\nPending")

    st.markdown("---")
    return current_step


def _organization_details_section(reg: Dict[str, Any]) -> None:
    org = reg["organization"]

    st.subheader("Organization Details")
    st.markdown(
        "Capture laboratory profile, working hours, and statutory details. This maps to Steps 1-10 in the LMS Organization Details module."
    )

    with st.form("org_details_form"):
        col1, col2 = st.columns(2)

        with col1:
            lab_name = st.text_input("Laboratory Name *", value=org["lab_name"])
            legal_name = st.text_input("Legal Entity Name", value=org["legal_name"])
            type_of_org = st.selectbox(
                "Type of Organization *",
                [
                    "",
                    "Proprietorship",
                    "Partnership",
                    "Private Limited",
                    "Public Limited",
                    "Government",
                    "Trust / Society",
                    "Other",
                ],
                index=0 if not org["type_of_org"] else 1,
            )
            parent_org = st.text_input("Parent Organization", value=org["parent_org"])
            contact_person = st.text_input("Top Management / Contact Person *", value=org["contact_person"])
            email = st.text_input("Official Email *", value=org["email"])

        with col2:
            address = st.text_area("Registered / Lab Address *", value=org["address"], height=100)
            city = st.text_input("City", value=org["city"])
            state_val = st.text_input("State", value=org["state"])
            country = st.text_input("Country", value=org["country"] or "India")
            phone = st.text_input("Primary Phone", value=org["phone"])
            working_days = st.text_input("Normal Working Days *", value=org["working_days"], placeholder="Mon-Fri")
            working_hours = st.text_input("Working Hours", value=org["working_hours"], placeholder="09:00 - 18:00")

        st.markdown("---")
        st.markdown("**Statutory & Accreditation Details**")
        col3, col4, col5 = st.columns(3)
        with col3:
            has_statutory_docs = st.checkbox(
                "Statutory compliance documents captured",
                value=org["has_statutory_docs"],
            )
        with col4:
            has_accreditation_docs = st.checkbox(
                "Accreditation / certification details captured",
                value=org["has_accreditation_docs"],
            )
        with col5:
            has_other_details = st.checkbox(
                "Other undertakings & policies noted",
                value=org["has_other_details"],
            )

        submitted = st.form_submit_button("Save organization details")
        if submitted:
            org.update(
                {
                    "lab_name": lab_name.strip(),
                    "legal_name": legal_name.strip(),
                    "type_of_org": type_of_org,
                    "parent_org": parent_org.strip(),
                    "contact_person": contact_person.strip(),
                    "email": email.strip(),
                    "address": address.strip(),
                    "city": city.strip(),
                    "state": state_val.strip(),
                    "country": country.strip(),
                    "phone": phone.strip(),
                    "working_days": working_days.strip(),
                    "working_hours": working_hours.strip(),
                    "has_statutory_docs": has_statutory_docs,
                    "has_accreditation_docs": has_accreditation_docs,
                    "has_other_details": has_other_details,
                }
            )
            st.success("Organization details saved for this demo session.")


def _scope_management_section(reg: Dict[str, Any]) -> None:
    scope = reg["scope"]

    st.subheader("Scope Management")
    st.markdown(
        "Define scope of recognition and manage key equipment. This mirrors the LMS Scope Management module in a concise way."
    )

    tab1, tab2 = st.tabs(["Scope of Recognition", "Lab Equipment"])

    with tab1:
        st.markdown("#### Indian Standards / Fields of Testing")

        if scope["scopes"]:
            st.table(scope["scopes"])
        else:
            st.info("No scope entries added yet. Use the form below to add your first Indian Standard.")

        st.markdown("---")
        st.markdown("**Add new scope entry**")
        with st.form("add_scope_form"):
            col1, col2 = st.columns(2)
            with col1:
                indian_standard = st.text_input("Indian Standard Number *", placeholder="e.g., IS 302-1")
                optimal_time = st.text_input("Optimal testing time", placeholder="e.g., 2 days")
            with col2:
                field_of_testing = st.selectbox(
                    "Field of Testing *",
                    [
                        "",
                        "Chemical",
                        "Mechanical",
                        "Electrical",
                        "Civil",
                        "Electronics",
                        "Environmental",
                        "Textile",
                        "Food & Agriculture",
                        "Medical",
                        "Other",
                    ],
                )
                capacity = st.text_input("Testing capacity per month", placeholder="e.g., 50 samples")

            add_scope = st.form_submit_button("Add scope")
            if add_scope:
                if not indian_standard.strip() or not field_of_testing:
                    st.error("Please fill in both Indian Standard and Field of Testing.")
                else:
                    new_scope = {
                        "id": int(datetime.utcnow().timestamp() * 1000),
                        "indian_standard": indian_standard.strip(),
                        "field_of_testing": field_of_testing,
                        "optimal_time": optimal_time.strip(),
                        "capacity_per_month": capacity.strip(),
                    }
                    scope["scopes"].append(new_scope)
                    st.success("Scope entry added.")

    with tab2:
        st.markdown("#### Key Lab Equipment")

        if scope["equipments"]:
            st.table(scope["equipments"])
        else:
            st.info("No equipment recorded yet. Use the form below to add equipment relevant to your scope.")

        st.markdown("---")
        st.markdown("**Add new equipment**")
        with st.form("add_equipment_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                name = st.text_input("Equipment name *", placeholder="e.g., Spectrum Analyzer")
                model = st.text_input("Model", placeholder="e.g., RSA306B")
            with col2:
                identification_number = st.text_input("Identification number *", placeholder="e.g., EQ-001")
                maintenance_type = st.selectbox(
                    "Maintenance type",
                    ["", "Internal", "External", "Both"],
                )
            with col3:
                calibration_date = st.date_input("Last calibration date", value=None, key="cal_date")
                validity_date = st.date_input("Calibration valid till", value=None, key="val_date")

            add_equipment = st.form_submit_button("Add equipment")
            if add_equipment:
                if not name.strip() or not identification_number.strip():
                    st.error("Please fill in at least equipment name and identification number.")
                else:
                    new_equipment = {
                        "id": int(datetime.utcnow().timestamp() * 1000),
                        "name": name.strip(),
                        "model": model.strip(),
                        "identification_number": identification_number.strip(),
                        "maintenance_type": maintenance_type,
                        "calibration_date": calibration_date.isoformat() if calibration_date else None,
                        "validity_date": validity_date.isoformat() if validity_date else None,
                    }
                    scope["equipments"].append(new_equipment)
                    st.success("Equipment added.")


def _manpower_section(reg: Dict[str, Any]) -> None:
    manpower = reg["manpower"]

    st.subheader("Manpower Management")
    st.markdown(
        "Capture key technical and quality personnel linked to your scope. This is a condensed version of the LMS Manpower module."
    )

    if manpower["personnel"]:
        st.markdown("#### Current personnel")
        for idx, p in enumerate(manpower["personnel"], start=1):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            with col1:
                st.markdown(f"**{idx}. {p['first_name']} {p['last_name']}**")
                st.caption(p.get("email", ""))
            with col2:
                st.text(f"Designation: {p.get('designation', '')}")
            with col3:
                st.text(f"Department: {p.get('department', '')}")
            with col4:
                st.text(f"Mobile: {p.get('mobile', '')}")
        st.markdown("---")
    else:
        st.info("No manpower added yet. Use the form below to add your first key person.")

    st.markdown("**Add new personnel**")
    with st.form("add_personnel_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First name *")
            last_name = st.text_input("Last name *")
            email = st.text_input("Email *")
            mobile = st.text_input("Mobile *", placeholder="Include country code if needed")
        with col2:
            designation = st.selectbox(
                "Designation level *",
                [
                    "",
                    "Technical Manager",
                    "Quality Manager",
                    "Lab Head",
                    "Lab Officer",
                    "Technical Assistant",
                    "Sample Cell",
                    "QA Officer",
                    "QC Testing",
                    "Other",
                ],
            )
            department = st.text_input("Department", placeholder="e.g., EMC Lab")
            role = st.text_input("Role", placeholder="e.g., Testing / Reporting")

        add_personnel = st.form_submit_button("Add personnel")
        if add_personnel:
            if not (first_name.strip() and last_name.strip() and email.strip() and mobile.strip() and designation):
                st.error("Please fill all required fields for personnel.")
            else:
                new_person = {
                    "id": int(datetime.utcnow().timestamp() * 1000),
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip(),
                    "email": email.strip(),
                    "mobile": mobile.strip(),
                    "designation": designation,
                    "department": department.strip(),
                    "role": role.strip(),
                }
                manpower["personnel"].append(new_person)
                st.success("Personnel added.")


def _checklist_section(reg: Dict[str, Any], statuses: Dict[str, bool]) -> None:
    st.subheader("Checklist & Payment Readiness")
    st.markdown(
        "Final validation view that summarizes completion of all registration sections, similar to the LMS Checklist step."
    )

    items = [
        {"id": 1, "subject": "Laboratory Details", "step": "Organization Details"},
        {"id": 2, "subject": "Registered / Head Office Address", "step": "Organization Details"},
        {"id": 3, "subject": "Top Management / Contact Person", "step": "Organization Details"},
        {"id": 4, "subject": "Normal Working Days & Hours", "step": "Organization Details"},
        {"id": 5, "subject": "Type of Organization", "step": "Organization Details"},
        {"id": 6, "subject": "Parent Organization", "step": "Organization Details"},
        {"id": 7, "subject": "Bank Details", "step": "Organization Details"},
        {"id": 8, "subject": "Statutory Compliance Documents", "step": "Organization Details"},
        {"id": 9, "subject": "Accreditation / Certification Details", "step": "Organization Details"},
        {"id": 10, "subject": "Other Details / Undertakings", "step": "Organization Details"},
        {"id": 11, "subject": "Inter Lab Comparison / PT", "step": "Scope Management"},
        {"id": 12, "subject": "Internal Audit & Management Review", "step": "Scope Management"},
        {"id": 13, "subject": "Scope of Recognition (Indian Standards)", "step": "Scope Management"},
        {"id": 14, "subject": "Lab Equipment", "step": "Scope Management"},
        {"id": 15, "subject": "Facilities Available", "step": "Scope Management"},
        {"id": 16, "subject": "Facilities Not Available / Exclusions", "step": "Scope Management"},
        {"id": 17, "subject": "Reference Materials", "step": "Scope Management"},
        {"id": 18, "subject": "Sample Testing Charges", "step": "Scope Management"},
        {"id": 19, "subject": "Lab Manpower", "step": "Manpower"},
        {"id": 20, "subject": "Overall Validation", "step": "Checklist"},
    ]

    completed_items = 0
    for item in items:
        step_label = item["step"]
        done = statuses.get(step_label, False)
        if done:
            completed_items += 1

    total_items = len(items)
    progress = completed_items / total_items if total_items else 0

    st.markdown("#### Progress overview")
    st.progress(progress)
    st.markdown(f"**{completed_items} of {total_items} checklist items are marked as completed based on the data above.**")

    st.markdown("---")
    st.markdown("#### Detailed checklist")

    for item in items:
        step_label = item["step"]
        done = statuses.get(step_label, False)
        col1, col2, col3, col4 = st.columns([0.7, 4, 2, 1.2])
        with col1:
            st.write(item["id"])
        with col2:
            st.write(item["subject"])
        with col3:
            if done:
                st.markdown("<span style='color: green; font-weight: 600;'>Completed</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color: #b45309; font-weight: 600;'>Pending</span>", unsafe_allow_html=True)
        with col4:
            if step_label != "Checklist":
                if st.button("Edit", key=f"edit_{item['id']}"):
                    st.session_state.lab_registration_current_step = step_label
                    st.experimental_rerun()

    st.markdown("---")
    st.markdown("#### Payment readiness")

    all_completed = statuses["Checklist"]
    if all_completed:
        st.success("All sections are complete. You are ready to proceed to payment in a production system.")
    else:
        st.info("Complete all sections above to enable payment.")

    st.button("Make payment (demo)", disabled=not all_completed)


# -------- Main Entrypoint -------- #

_init_lab_registration_state()
registration = _get_lab_registration()
step_labels_order = ["Organization Details", "Scope Management", "Manpower", "Checklist"]
step_statuses = _compute_step_statuses(registration)

current_step_label = _render_step_header(step_labels_order, step_statuses)

if current_step_label == "Organization Details":
    _organization_details_section(registration)
elif current_step_label == "Scope Management":
    _scope_management_section(registration)
elif current_step_label == "Manpower":
    _manpower_section(registration)
else:
    _checklist_section(registration, step_statuses)
