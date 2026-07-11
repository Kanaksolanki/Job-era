import streamlit as st
import requests

BACKEND_URL = "https://jobera-0f9j.onrender.com"

st.set_page_config(page_title="Internship Suggestions", layout="wide")

st.title(" Internship Suggestions")

# -------------------------------
# Check if job selected
# -------------------------------
if "selected_job" not in st.session_state:
    st.warning(" No job selected.")
    if st.button(" Go Back"):
        st.switch_page("Job_Recommendations.py")
    st.stop()

job = st.session_state["selected_job"]
if "last_job" not in st.session_state or st.session_state["last_job"] != job["title"]:
    st.session_state.pop("skill_gap", None)
    st.session_state["last_job"] = job["title"]

# -------------------------------
# Job Info (optional but useful)
# -------------------------------
st.markdown(f"## {job['title']}")
st.info(f" Match Score: {job['match_score']}")
st.write("**Your Skills:**", ", ".join(job["matched_skills"]))

# -------------------------------
# Use cached skill gap if available
# -------------------------------
if "skill_gap" in st.session_state:
    data = st.session_state["skill_gap"]
else:
    with st.spinner("Fetching internships..."):
        response = requests.post(
            f"{BACKEND_URL}/api/skill-gap",
            json={
                "role": job["title"],
                "skills": job["matched_skills"]
            }
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state["skill_gap"] = data
        else:
            st.error(" Failed to fetch internships")
            st.stop()

# -------------------------------
# Show Internships
# -------------------------------
if data.get("internships"):
    st.markdown("## Recommended Internships")

    for internship in data["internships"]:
        link = internship.get("link", "#")

        link_html = (
            f'<a href="{link}" target="_blank" style="color:#4CAF50;">🔗 Apply Now</a>'
            if link != "#"
            else '<p style="color:gray;">No link available</p>'
        )

        st.markdown(f"""
        <div style="
            padding:15px;
            border-radius:12px;
            background-color:#1e1e2f;
            margin-bottom:12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        ">
            <h4 style="color:#4CAF50;">{internship.get('title', 'Internship')}</h4>
            <p><b>Platform:</b> {internship.get('platform', 'N/A')}</p>
            {link_html}
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("No internships found for this role.")

# -------------------------------
# Navigation Buttons
# -------------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button(" Back to Jobs", key="back_to_jobs_intern", use_container_width=True):
        st.switch_page("Job_Recommendations.py")

with col2:
    if st.button(" View Projects", key="view_projects_from_intern", use_container_width=True):
        st.switch_page("pages/3_Project_Suggestions.py")