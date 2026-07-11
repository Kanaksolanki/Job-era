print("ROUTES FILE LOADED")
from flask import Blueprint, request, jsonify
from pdf_extractor import extract_text_from_pdf
from preprocessor import extract_features
from recommender import recommend_jobs
import sys
import os

# Add parent folder (backend) to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from skill_gap.skill_gap import get_skill_gap
from skill_gap.llm_module import get_course_suggestions

api_bp = Blueprint("api", __name__)

ALLOWED_EXTENSION = "pdf"


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() == ALLOWED_EXTENSION


# ─────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────
@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Job Recommender API"})


# ─────────────────────────────────────────
# Resume → Job Recommendations
# ─────────────────────────────────────────
@api_bp.route("/recommend", methods=["POST"])
def recommend():
    if "resume" not in request.files:
        return jsonify({"error": "No file provided. Send the PDF under the key 'resume'."}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "Empty filename."}), 400

    if not _allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are accepted."}), 400

    try:
        top_n = int(request.args.get("top_n", 5))
        top_n = max(1, min(top_n, 10))
    except ValueError:
        top_n = 5

    try:
        file_bytes = file.read()
        raw_text = extract_text_from_pdf(file_bytes)
        features = extract_features(raw_text)
        recommendations = recommend_jobs(features, top_n=top_n)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 422
    except Exception as e:
        return jsonify({"error": f"Internal processing error: {str(e)}"}), 500

    filtered = [
        {
            "title": r["title"],
            "match_score": r["match_score"],
            "matched_skills": r.get("matched_skills", [])
        }
        for r in recommendations
    ]

    return jsonify(filtered), 200


# ─────────────────────────────────────────
# ✅ NEW: Skill Gap (called by frontend)
# ─────────────────────────────────────────

@api_bp.route("/skill-gap", methods=["POST"])
def skill_gap():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No JSON body provided"}), 400

        role = data.get("role", "").strip()
        user_skills = data.get("skills", [])

        if not role:
            return jsonify({"error": "Role is required"}), 400

        # ✅ Normalize skills to match JOB_PROFILES domain format
        user_skills = [
            s.lower().strip().replace(" ", "_").replace("-", "_")
            for s in user_skills
        ]

        print(f"📥 Role: {role} | Skills: {user_skills}")  # shows in Render logs

        skill_gap_data = get_skill_gap(role, user_skills)

        if "error" in skill_gap_data:
            return jsonify(skill_gap_data), 400

        suggestions = get_course_suggestions(skill_gap_data)

        return jsonify({
            "role": skill_gap_data.get("role"),
            "match_percentage": skill_gap_data.get("match_percentage", 0),
            "missing_required_skills": skill_gap_data.get("missing_required_skills", []),
            "missing_preferred_skills": skill_gap_data.get("missing_preferred_skills", []),
            "courses": suggestions.get("courses", []),
            "projects": suggestions.get("projects", []),
            "internships": suggestions.get("internships", []),
            "roadmap": suggestions.get("roadmap", [])
        }), 200

    except Exception as e:
        print(f"🔥 /skill-gap ERROR: {str(e)}")
        import traceback
        traceback.print_exc()  # ✅ Full error in Render logs
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# Course Suggestions (standalone endpoint)
# ─────────────────────────────────────────
@api_bp.route("/course-suggestions", methods=["POST"])
def course_suggestions():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No JSON body provided"}), 400

        user_skills = data.get("user_skills", [])
        role = data.get("job_role", "").strip()

        if not role:
            return jsonify({"error": "Job role is required"}), 400

        skill_gap_data = get_skill_gap(role, user_skills)

        if "error" in skill_gap_data:
            return jsonify(skill_gap_data), 400

        courses = get_course_suggestions(skill_gap_data)

        return jsonify({
            "skill_gap": skill_gap_data,
            "courses": courses
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
