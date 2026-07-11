from dotenv import load_dotenv
import os
import json
import requests
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=False)


def get_course_suggestions(skill_gap_data):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("❌ OPENROUTER_API_KEY not set")
        return {
            "courses": [],
            "projects": [],
            "roadmap": [],
            "internships": [],
            "error": "API key not configured on server"
        }

    missing_required = skill_gap_data.get("missing_required_skills", [])
    missing_preferred = skill_gap_data.get("missing_preferred_skills", [])
    role = skill_gap_data.get("role", "Unknown Role")
    user_skills = skill_gap_data.get("user_skills", [])

    prompt = f"""
    You are an expert AI career mentor.

    Target Role: {role}
    User Skills: {user_skills}
    Missing Required Skills: {missing_required}
    Missing Preferred Skills: {missing_preferred}

    Return ONLY valid JSON. No explanation, no markdown, no extra text.

    FORMAT:
    {{
      "courses": [
        {{
          "course_name": "",
          "platform": "",
          "skill_covered": "",
          "link": ""
        }}
      ],
      "projects": [
        {{
          "project_name": "",
          "description": "",
          "link": ""
        }}
      ],
      "roadmap": [
        {{
          "step": 1,
          "description": ""
        }}
      ],
      "internships": [
        {{
          "title": "",
          "platform": "",
          "link": ""
        }}
      ]
    }}

    Rules:
    - Give 3 to 5 courses
    - Give 2 to 3 projects
    - Roadmap must be step-by-step
    - Return clean JSON only, no markdown fences
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openrouter/free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=90
        )

        if response.status_code != 200:
            raise ValueError(f"OpenRouter error {response.status_code}: {response.text}")

        result = response.json()
        raw_text = result["choices"][0]["message"]["content"].strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(raw_text)

        return {
            "courses": parsed.get("courses", []),
            "projects": parsed.get("projects", []),
            "roadmap": parsed.get("roadmap", []),
            "internships": parsed.get("internships", [])
        }

    except json.JSONDecodeError as e:
        print(f"🔥 JSON PARSE ERROR: {str(e)}")
        return {
            "courses": [], "projects": [], "roadmap": [], "internships": [],
            "error": f"Failed to parse LLM response: {str(e)}"
        }

    except Exception as e:
        print(f"🔥 LLM ERROR: {str(e)}")
        return {
            "courses": [], "projects": [], "roadmap": [], "internships": [],
            "error": str(e)
        }