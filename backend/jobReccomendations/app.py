import os
import sys

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.jobReccomendations.pdf_extractor import extract_text_from_pdf
from backend.jobReccomendations.preprocessor import extract_features
from backend.jobReccomendations.recommender import JOB_PROFILES, recommend_jobs
from backend.skill_gap.skill_gap import get_skill_gap
from backend.skill_gap.llm_module import get_course_suggestions

ALLOWED_EXTENSION = "pdf"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "Career Assistant API"}), 200

    @app.route("/api/recommend", methods=["POST"])
    def recommend():
        if "resume" not in request.files:
            return jsonify({"error": "No file provided."}), 400

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
            raw_text = extract_text_from_pdf(file.read())
            features = extract_features(raw_text)
            recommendations = recommend_jobs(features, top_n=top_n)
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 422
        except Exception as exc:
            return jsonify({"error": f"Internal processing error: {str(exc)}"}), 500

        response = [
            {
                "title": item["title"],
                "match_score": item["match_score"],
                "matched_skills": item["matched_skills"],
            }
            for item in recommendations
        ]
        return jsonify(response), 200

    @app.route("/api/skill-gap", methods=["POST"])
    def skill_gap():
        try:
            payload = request.get_json(silent=True)
            if not payload:
                return jsonify({"error": "Invalid JSON payload."}), 400

            role = payload.get("role", "").strip()
            user_skills = payload.get("skills", [])

            if not role:
                return jsonify({"error": "Role must be provided."}), 400
            if not isinstance(user_skills, list):
                return jsonify({"error": "Skills must be a list."}), 400

            # Normalize skills
            user_skills = [
                s.lower().strip().replace(" ", "_").replace("-", "_")
                for s in user_skills
            ]

            print(f"📥 Role: {role} | Skills: {user_skills}")

            # Step 1: Compute skill gap (no LLM)
            gap = get_skill_gap(role, user_skills)

            if "error" in gap:
                return jsonify(gap), 400

            # Step 2: Single LLM call with correct keys
            llm_input = {
                "role": role,
                "user_skills": user_skills,
                "missing_required_skills": gap.get("missing_required_skills", []),
                "missing_preferred_skills": gap.get("missing_preferred_skills", [])
            }

            suggestions = get_course_suggestions(llm_input)

            # Step 3: Return merged response
            return jsonify({
                "role": gap["role"],
                "match_percentage": gap["match_percentage"],
                "missing_required_skills": gap["missing_required_skills"],
                "missing_preferred_skills": gap["missing_preferred_skills"],
                "courses": suggestions.get("courses", []),
                "projects": suggestions.get("projects", []),
                "internships": suggestions.get("internships", []),
                "roadmap": suggestions.get("roadmap", [])
            }), 200

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"🔥 /api/skill-gap ERROR: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/job-roles", methods=["GET"])
    def job_roles():
        return jsonify([
            {
                "title": job["title"],
                "required_domains": job["required_domains"],
                "preferred_domains": job.get("preferred_domains", []),
            }
            for job in JOB_PROFILES
        ]), 200

    return app


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() == ALLOWED_EXTENSION


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
