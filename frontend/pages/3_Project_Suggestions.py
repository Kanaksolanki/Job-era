import streamlit as st
import requests

BACKEND_URL = "https://jobera-0f9j.onrender.com"

st.set_page_config(page_title="Project Suggestions", layout="wide")

st.title(" Project Suggestions")

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
# Job Info
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
    with st.spinner("Fetching project ideas..."):
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
            st.error(" Failed to fetch projects")
            st.stop()

# -------------------------------
# Show Projects
# -------------------------------
if data.get("projects"):
    st.markdown("## Recommended Projects")

    for project in data["projects"]:
        link = project.get("link", "#")

        link_html = (
            f'<a href="{link}" target="_blank" style="color:#4CAF50;">🔗 View Project</a>'
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
            <h4 style="color:#4CAF50;">{project.get('project_name', 'Project')}</h4>
            <p><b>Description:</b> {project.get('description', 'N/A')}</p>
            {link_html}
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("No project suggestions found for this role.")

# -------------------------------
# Navigation Buttons
# -------------------------------
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button(" Back to Jobs", key="back_to_jobs_proj", use_container_width=True):
        st.switch_page("Job_Recommendations.py")

with col2:
    if st.button(" View Internships", key="view_internships_from_proj", use_container_width=True):
        st.switch_page("pages/2_Internship_Suggestions.py")