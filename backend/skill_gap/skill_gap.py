from backend.jobReccomendations.recommender import JOB_PROFILES


def normalize_skill(skill: str) -> str:
    return skill.lower().strip().replace(" ", "_").replace("-", "_")


def get_role_data(role):
    for job in JOB_PROFILES:
        if job["title"].lower() == role.lower():
            return job
    return None


def get_skill_gap(role, user_skills):
    job = get_role_data(role)

    if not job:
        return {"error": "Role not found"}

    required_skills = job.get("required_domains", [])
    preferred_skills = job.get("preferred_domains", [])

    user_skills_normalized = set(normalize_skill(s) for s in user_skills)
    required_skills_normalized = [normalize_skill(s) for s in required_skills]
    preferred_skills_normalized = [normalize_skill(s) for s in preferred_skills]

    missing_required = list(set(required_skills_normalized) - user_skills_normalized)
    missing_preferred = list(set(preferred_skills_normalized) - user_skills_normalized)

    match_percentage = 0
    if required_skills_normalized:
        matched = user_skills_normalized.intersection(set(required_skills_normalized))
        match_percentage = (len(matched) / len(required_skills_normalized)) * 100

    return {
        "role": role,
        "missing_required_skills": missing_required,
        "missing_preferred_skills": missing_preferred,
        "match_percentage": round(match_percentage, 2)
    }