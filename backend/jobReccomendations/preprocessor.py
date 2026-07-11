
import re
import string
from typing import Dict, List, Set

_STOPWORDS: Set[str] = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "he", "him", "his", "himself", "she", "her", "hers",
    "herself", "it", "its", "itself", "they", "them", "their", "theirs",
    "themselves", "what", "which", "who", "whom", "this", "that", "these",
    "those", "am", "is", "are", "was", "were", "be", "been", "being", "have",
    "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the",
    "and", "but", "if", "or", "because", "as", "until", "while", "of", "at",
    "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "s", "t", "can",
    "will", "just", "don", "should", "now", "d", "ll", "m", "o", "re", "ve",
    "y", "ain", "aren", "couldn", "didn", "doesn", "hadn", "hasn", "haven",
    "isn", "ma", "mightn", "mustn", "needn", "shan", "shouldn", "wasn",
    "weren", "won", "wouldn", "use", "using", "used", "work", "worked",
    "working", "experience", "knowledge", "ability", "strong", "good", "well",
    "also", "etc", "including", "excellent", "various", "within", "across",
    "multiple", "high", "new", "large", "based", "key", "responsible",
    "required", "preferred", "proficient"
}

SKILL_KEYWORDS: Dict[str, List[str]] = {
    # Programming languages
    "python": ["python", "django", "flask", "fastapi", "pandas", "numpy", "scipy"],
    "javascript": ["javascript", "js", "typescript", "ts", "node", "nodejs", "react",
                   "reactjs", "angular", "vue", "vuejs", "nextjs", "express"],
    "java": ["java", "spring", "springboot", "hibernate", "maven", "gradle"],
    "c_cpp": ["c++", "cpp", "c#", "csharp", ".net", "dotnet", "unity"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite", "oracle", "mssql",
            "t-sql", "plsql", "nosql", "mongodb", "redis", "cassandra", "dynamodb"],
    "r_language": ["r programming", "rstudio", "ggplot", "dplyr", "tidyr"],
    "scala": ["scala", "spark", "akka"],
    "go": ["golang", "go language"],
    "rust": ["rust"],
    "php": ["php", "laravel", "symfony", "wordpress"],
    "ruby": ["ruby", "rails", "ruby on rails"],
    "swift": ["swift", "ios", "xcode", "swiftui"],
    "kotlin": ["kotlin", "android"],
    "shell": ["bash", "shell scripting", "powershell", "zsh"],

    # ML / AI / Data Science
    "machine_learning": ["machine learning", "ml", "supervised", "unsupervised",
                         "classification", "regression", "clustering", "random forest",
                         "gradient boosting", "xgboost", "lightgbm", "svm", "neural network",
                         "deep learning", "cnn", "rnn", "lstm", "transformer", "bert", "gpt",
                         "llm", "nlp", "natural language processing", "computer vision",
                         "reinforcement learning"],
    "data_science": ["data science", "data analysis", "data analytics", "statistics",
                     "hypothesis testing", "a/b testing", "feature engineering",
                     "exploratory data analysis", "eda", "data visualization"],
    "ml_frameworks": ["tensorflow", "keras", "pytorch", "scikit-learn", "sklearn",
                      "hugging face", "transformers", "opencv", "spacy", "nltk", "gensim"],
    "data_engineering": ["etl", "data pipeline", "airflow", "kafka", "spark", "hadoop",
                         "hive", "flink", "dbt", "data warehouse", "data lake",
                         "snowflake", "bigquery", "redshift"],

    # Cloud & DevOps
    "cloud": ["aws", "amazon web services", "azure", "google cloud", "gcp",
              "ec2", "s3", "lambda", "cloudformation", "terraform", "pulumi"],
    "devops": ["devops", "ci/cd", "jenkins", "github actions", "gitlab ci",
               "docker", "kubernetes", "k8s", "helm", "ansible", "chef", "puppet",
               "linux", "unix", "nginx", "apache"],

    # Web / Backend
    "web_development": ["html", "css", "sass", "tailwind", "bootstrap", "rest api",
                        "restful", "graphql", "websocket", "microservices", "api design",
                        "oauth", "jwt"],

    # Databases
    "databases": ["database", "dbms", "schema design", "query optimization",
                  "stored procedures", "indexing", "normalization"],

    # Cybersecurity
    "security": ["cybersecurity", "penetration testing", "ethical hacking", "soc",
                 "siem", "firewall", "network security", "vulnerability assessment",
                 "owasp", "encryption", "pki", "iam"],

    # Design & UX
    "design": ["ui/ux", "ux design", "user experience", "figma", "sketch", "adobe xd",
               "illustrator", "photoshop", "wireframing", "prototyping", "user research"],

    # Project management & Soft skills
    "project_management": ["agile", "scrum", "kanban", "jira", "confluence",
                           "project management", "pmp", "product management",
                           "stakeholder management", "roadmap"],

    # Finance / Business
    "finance": ["financial modeling", "excel", "vba", "bloomberg", "valuation",
                "accounting", "cfa", "investment banking", "portfolio management",
                "risk management", "derivatives", "equity"],

    # Marketing / SEO
    "marketing": ["seo", "sem", "google analytics", "google ads", "meta ads",
                  "content marketing", "social media", "email marketing",
                  "copywriting", "crm", "salesforce", "hubspot"],

    # Healthcare / Biology
    "healthcare": ["clinical", "ehr", "fhir", "hl7", "hipaa", "medical imaging",
                   "bioinformatics", "genomics", "clinical trials", "pharma"],

    # Embedded / Hardware
    "embedded": ["embedded systems", "iot", "arduino", "raspberry pi", "fpga",
                 "rtos", "firmware", "verilog", "vhdl", "pcb design"],
}

_EDUCATION_PATTERNS: Dict[str, str] = {
    "phd": r"\b(ph\.?d|doctor of philosophy|doctorate)\b",
    "masters": r"\b(m\.?s|m\.?e|m\.?tech|msc|master[s]? of (science|engineering|arts|business|technology)|mba|m\.?b\.?a)\b",
    "bachelors": r"\b(b\.?s|b\.?e|b\.?tech|b\.?sc|bachelor[s]? of (science|engineering|arts|technology|commerce)|b\.?c\.?a|b\.?c\.?s)\b",
    "diploma": r"\b(diploma|associate[s]?|hnd)\b",
    "high_school": r"\b(high school|secondary school|12th|xii|hssc)\b",
}

_EXPERIENCE_PATTERNS = [
    r"(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)",
    r"experience[:\s]+(\d+)\+?\s*years?",
    r"(\d+)\s*-\s*(\d+)\s*years?\s*(of\s*)?(experience|exp)",
]


def clean_text(text: str) -> str:
    """Lowercase, remove punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s/\.\+#]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_features(raw_text: str) -> Dict:
    cleaned = clean_text(raw_text)
    tokens = [t for t in cleaned.split() if t not in _STOPWORDS and len(t) > 1]

    skills = _extract_skills(cleaned)
    education = _extract_education(cleaned)
    experience = _extract_experience(cleaned)

    return {
        "cleaned_text": cleaned,
        "tokens": tokens,
        "skills": skills,
        "skill_domains": list(skills.keys()),
        "education_level": education,
        "years_experience": experience,
    }


def _extract_skills(cleaned_text: str) -> Dict[str, List[str]]:
    """Match skill keywords in cleaned text."""
    matched: Dict[str, List[str]] = {}
    for domain, keywords in SKILL_KEYWORDS.items():
        found = [kw for kw in keywords if kw in cleaned_text]
        if found:
            matched[domain] = found
    return matched


def _extract_education(cleaned_text: str) -> str:
    """Detect the highest education level mentioned."""
    for level, pattern in _EDUCATION_PATTERNS.items():
        if re.search(pattern, cleaned_text, re.IGNORECASE):
            return level
    return "unknown"


def _extract_experience(cleaned_text: str) -> int | None:
    """Extract max years of experience mentioned."""
    years = []
    for pattern in _EXPERIENCE_PATTERNS:
        for match in re.finditer(pattern, cleaned_text, re.IGNORECASE):
            for grp in match.groups():
                if grp and grp.isdigit():
                    years.append(int(grp))
    return max(years) if years else None
