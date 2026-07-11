
from __future__ import annotations
import math
import re
from collections import Counter
from typing import Dict, List, Tuple


JOB_PROFILES: List[Dict] = [
    # Software Engineering 
    {
        "title": "Backend Software Engineer",
        "required_domains": ["python", "sql", "web_development"],
        "preferred_domains": ["devops", "cloud", "databases"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "python django flask fastapi rest api microservices sql postgresql "
            "mysql database design backend server side development git linux "
            "docker api integration unit testing"
        ),
    },
    {
        "title": "Frontend Developer",
        "required_domains": ["javascript", "web_development"],
        "preferred_domains": ["design"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "javascript react angular vue html css typescript frontend ui "
            "responsive design browser api state management redux rest api "
            "webpack vite performance optimization accessibility"
        ),
    },
    {
        "title": "Full Stack Developer",
        "required_domains": ["javascript", "web_development"],
        "preferred_domains": ["python", "sql", "devops"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "full stack javascript react nodejs express python django rest api "
            "html css sql mongodb postgresql git docker deployment "
            "frontend backend integration ci cd agile"
        ),
    },
    {
        "title": "Mobile App Developer (Android/iOS)",
        "required_domains": ["kotlin", "swift"],
        "preferred_domains": ["java", "javascript"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "android kotlin java ios swift swiftui mobile development "
            "flutter react native app store play store api integration "
            "firebase mobile ui push notifications"
        ),
    },
    {
        "title": "DevOps / Cloud Engineer",
        "required_domains": ["devops", "cloud"],
        "preferred_domains": ["python", "shell"],
        "min_experience": 1,
        "min_education": "bachelors",
        "description": (
            "devops aws azure gcp docker kubernetes helm ci cd jenkins "
            "github actions terraform ansible infrastructure as code "
            "linux bash scripting monitoring prometheus grafana site reliability"
        ),
    },
    {
        "title": "Site Reliability Engineer (SRE)",
        "required_domains": ["devops", "cloud", "shell"],
        "preferred_domains": ["python", "databases"],
        "min_experience": 2,
        "min_education": "bachelors",
        "description": (
            "sre site reliability engineering kubernetes docker monitoring "
            "alerting on call incident management linux bash python automation "
            "availability scalability latency performance distributed systems"
        ),
    },

    # Data / AI 
    {
        "title": "Data Scientist",
        "required_domains": ["data_science", "machine_learning"],
        "preferred_domains": ["python", "sql", "ml_frameworks"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "data science machine learning statistics python pandas numpy "
            "scikit-learn model building evaluation feature engineering "
            "exploratory data analysis visualization matplotlib seaborn "
            "hypothesis testing regression classification clustering"
        ),
    },
    {
        "title": "Machine Learning Engineer",
        "required_domains": ["machine_learning", "ml_frameworks"],
        "preferred_domains": ["python", "data_engineering", "cloud"],
        "min_experience": 1,
        "min_education": "bachelors",
        "description": (
            "machine learning engineer mlops tensorflow pytorch deep learning "
            "model deployment model serving api production pipeline feature store "
            "training infrastructure gpu cuda distributed training"
        ),
    },
    {
        "title": "Data Analyst",
        "required_domains": ["data_science", "sql"],
        "preferred_domains": ["python", "r_language"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "data analyst sql excel power bi tableau data visualization "
            "business intelligence reporting dashboards kpi metrics "
            "data cleaning data wrangling python pandas statistics"
        ),
    },
    {
        "title": "Data Engineer",
        "required_domains": ["data_engineering", "sql"],
        "preferred_domains": ["python", "cloud", "scala"],
        "min_experience": 1,
        "min_education": "bachelors",
        "description": (
            "data engineer etl pipeline apache spark kafka airflow hadoop "
            "sql python scala data warehouse data lake snowflake bigquery "
            "redshift dbt streaming batch processing"
        ),
    },
    {
        "title": "NLP Engineer",
        "required_domains": ["machine_learning", "ml_frameworks"],
        "preferred_domains": ["python", "data_science"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "nlp natural language processing text mining bert gpt transformers "
            "hugging face spacy nltk gensim text classification ner "
            "sentiment analysis information extraction llm fine tuning"
        ),
    },
    {
        "title": "Computer Vision Engineer",
        "required_domains": ["machine_learning", "ml_frameworks"],
        "preferred_domains": ["python", "embedded"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "computer vision opencv pytorch tensorflow image processing "
            "object detection segmentation cnn feature extraction yolo "
            "video analytics image classification deep learning"
        ),
    },
    {
        "title": "AI Research Scientist",
        "required_domains": ["machine_learning", "ml_frameworks", "data_science"],
        "preferred_domains": ["python", "r_language"],
        "min_experience": 2,
        "min_education": "masters",
        "description": (
            "research scientist deep learning reinforcement learning generative models "
            "gans diffusion models llm pretraining finetuning arxiv publications "
            "pytorch tensorflow statistical learning theory phd"
        ),
    },

    # Cybersecurity
    {
        "title": "Cybersecurity Analyst",
        "required_domains": ["security"],
        "preferred_domains": ["devops", "shell"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "cybersecurity soc analyst siem splunk threat detection incident response "
            "vulnerability scanning penetration testing network security "
            "firewall ids ips owasp ethical hacking"
        ),
    },
    {
        "title": "Penetration Tester",
        "required_domains": ["security", "shell"],
        "preferred_domains": ["c_cpp", "python"],
        "min_experience": 1,
        "min_education": "bachelors",
        "description": (
            "penetration testing ethical hacking red team metasploit burp suite "
            "nmap wireshark exploit development vulnerability assessment "
            "ceh oscp ctf linux bash python web application security"
        ),
    },

    # Design / UX
    {
        "title": "UI/UX Designer",
        "required_domains": ["design"],
        "preferred_domains": ["javascript", "web_development"],
        "min_experience": None,
        "min_education": None,
        "description": (
            "ui ux design figma sketch adobe xd wireframing prototyping "
            "user research usability testing design system component library "
            "interaction design information architecture accessibility"
        ),
    },

    # Embedded / Hardware
    {
        "title": "Embedded Systems Engineer",
        "required_domains": ["embedded"],
        "preferred_domains": ["c_cpp", "shell"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "embedded systems firmware c c++ rtos microcontroller arduino "
            "raspberry pi iot fpga verilog vhdl pcb circuit design "
            "uart spi i2c real time operating system"
        ),
    },

    # Finance / Quant
    {
        "title": "Financial Analyst",
        "required_domains": ["finance"],
        "preferred_domains": ["data_science", "sql"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "financial analyst excel financial modeling valuation dcf lbo "
            "bloomberg equity research portfolio management investment banking "
            "accounting cfa chartered financial analyst reporting"
        ),
    },
    {
        "title": "Quantitative Analyst (Quant)",
        "required_domains": ["finance", "machine_learning"],
        "preferred_domains": ["python", "r_language", "data_science"],
        "min_experience": None,
        "min_education": "masters",
        "description": (
            "quantitative analyst quant python r stochastic calculus "
            "derivatives pricing risk management algorithmic trading "
            "statistics time series mathematical finance"
        ),
    },

    #  Marketing / Growth
    {
        "title": "Digital Marketing Analyst",
        "required_domains": ["marketing"],
        "preferred_domains": ["data_science", "sql"],
        "min_experience": None,
        "min_education": None,
        "description": (
            "digital marketing seo sem google analytics google ads "
            "facebook ads social media marketing content strategy "
            "email campaigns crm hubspot salesforce marketing analytics"
        ),
    },

    # Project Management 
    {
        "title": "Technical Project Manager",
        "required_domains": ["project_management"],
        "preferred_domains": ["devops", "web_development"],
        "min_experience": 2,
        "min_education": None,
        "description": (
            "project manager agile scrum kanban jira confluence "
            "stakeholder management sprint planning roadmap delivery "
            "risk management technical team budget tracking pmp"
        ),
    },
    {
        "title": "Product Manager",
        "required_domains": ["project_management"],
        "preferred_domains": ["data_science", "marketing"],
        "min_experience": 2,
        "min_education": "bachelors",
        "description": (
            "product manager product roadmap user stories backlog "
            "agile scrum stakeholder alignment go to market strategy "
            "kpi metrics product analytics a/b testing customer research"
        ),
    },

    # Healthcare / Bio 
    {
        "title": "Health Informatics / Clinical Data Analyst",
        "required_domains": ["healthcare"],
        "preferred_domains": ["data_science", "sql"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "health informatics ehr fhir hl7 hipaa clinical data "
            "medical records patient data sql python healthcare analytics "
            "epic cerner clinical trials bioinformatics"
        ),
    },

    #  General Software Roles
    {
        "title": "Software Quality Assurance (QA) Engineer",
        "required_domains": ["web_development"],
        "preferred_domains": ["python", "javascript", "devops"],
        "min_experience": None,
        "min_education": "bachelors",
        "description": (
            "qa engineer software testing manual testing automated testing "
            "selenium pytest junit test cases regression testing "
            "api testing postman jira bug tracking agile"
        ),
    },
    {
        "title": "Database Administrator (DBA)",
        "required_domains": ["sql", "databases"],
        "preferred_domains": ["shell", "devops"],
        "min_experience": 1,
        "min_education": "bachelors",
        "description": (
            "database administrator dba postgresql mysql oracle mssql "
            "performance tuning query optimization backup recovery "
            "replication high availability indexing stored procedures"
        ),
    },
]


# Education Hierarchy
_EDU_RANK: Dict[str, int] = {
    "unknown": 0,
    "high_school": 1,
    "diploma": 2,
    "bachelors": 3,
    "masters": 4,
    "phd": 5,
}


#TF-IDF

def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _tf(tokens: List[str]) -> Dict[str, float]:
    counts = Counter(tokens)
    total = len(tokens) or 1
    return {t: c / total for t, c in counts.items()}


def _idf(corpus: List[List[str]]) -> Dict[str, float]:
    N = len(corpus)
    df: Dict[str, int] = {}
    for doc in corpus:
        for term in set(doc):
            df[term] = df.get(term, 0) + 1
    return {t: math.log((N + 1) / (d + 1)) + 1 for t, d in df.items()}


def _tfidf_vector(tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
    tf = _tf(tokens)
    return {t: tf[t] * idf.get(t, 1.0) for t in tf}


def _cosine(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    common = set(v1) & set(v2)
    if not common:
        return 0.0
    dot = sum(v1[t] * v2[t] for t in common)
    mag1 = math.sqrt(sum(x ** 2 for x in v1.values()))
    mag2 = math.sqrt(sum(x ** 2 for x in v2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


#Main Recommender 

def recommend_jobs(features: Dict, top_n: int = 5) -> List[Dict]:
    resume_text = features["cleaned_text"]
    resume_tokens = _tokenize(resume_text)
    skill_domains: List[str] = features["skill_domains"]
    skills: Dict = features["skills"]
    edu_level: str = features["education_level"]
    years_exp: int | None = features["years_experience"]
    job_desc_tokens = [_tokenize(j["description"]) for j in JOB_PROFILES]
    corpus = [resume_tokens] + job_desc_tokens
    idf = _idf(corpus)

    resume_vec = _tfidf_vector(resume_tokens, idf)
    job_vecs = [_tfidf_vector(t, idf) for t in job_desc_tokens]

    results: List[Dict] = []

    for idx, job in enumerate(JOB_PROFILES):
        required = set(job["required_domains"])
        preferred = set(job.get("preferred_domains", []))
        all_expected = required | preferred

        matched_required = required & set(skill_domains)
        matched_preferred = preferred & set(skill_domains)

        if not all_expected:
            domain_score = 0.0
        else:
            numerator = len(matched_required) * 2 + len(matched_preferred)
            denominator = len(required) * 2 + len(preferred)
            domain_score = numerator / denominator if denominator else 0.0

  
        tfidf_score = _cosine(resume_vec, job_vecs[idx])


        edu_penalty = 0.0
        if job.get("min_education"):
            required_edu_rank = _EDU_RANK.get(job["min_education"], 0)
            user_edu_rank = _EDU_RANK.get(edu_level, 0)
            if user_edu_rank < required_edu_rank:
                edu_penalty = 0.15 

        exp_penalty = 0.0
        min_exp = job.get("min_experience")
        if min_exp and years_exp is not None and years_exp < min_exp:
            exp_penalty = 0.10
        raw_score = 0.60 * domain_score + 0.40 * tfidf_score
        final_score = max(0.0, raw_score - edu_penalty - exp_penalty)

        matched_skill_keywords: List[str] = []
        for domain in (matched_required | matched_preferred):
            matched_skill_keywords.extend(skills.get(domain, []))
        reasoning = _build_reasoning(
            job, matched_required, matched_preferred,
            edu_level, years_exp, edu_penalty, exp_penalty
        )

        results.append(
            {
                "title": job["title"],
                "match_score": round(final_score * 100, 1),  # percent
                "matched_skills": list(set(matched_skill_keywords))[:15],
                "required_domains_matched": sorted(matched_required),
                "preferred_domains_matched": sorted(matched_preferred),
                "reasoning": reasoning,
            }
        )
    results.sort(key=lambda r: r["match_score"], reverse=True)
    return results[:top_n]


def _build_reasoning(
    job: Dict,
    matched_required: set,
    matched_preferred: set,
    edu_level: str,
    years_exp: int | None,
    edu_penalty: float,
    exp_penalty: float,
) -> str:
    parts = []
    if matched_required:
        parts.append(
            f"You match {len(matched_required)}/{len(job['required_domains'])} "
            f"core skill areas: {', '.join(sorted(matched_required))}."
        )
    else:
        parts.append("No core skill domains matched directly.")
    if matched_preferred:
        parts.append(
            f"Bonus match on: {', '.join(sorted(matched_preferred))}."
        )
    if edu_penalty > 0:
        parts.append(
            f"Note: This role typically requires a {job['min_education']} degree; "
            f"your detected level is {edu_level}."
        )
    if exp_penalty > 0:
        parts.append(
            f"Note: This role typically requires {job['min_experience']}+ years of experience."
        )
    return " ".join(parts) if parts else "Matched based on overall profile similarity."
