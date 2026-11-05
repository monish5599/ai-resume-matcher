
import re
import json
import ollama


# =====================================================
# 1. NORMALIZE SKILL NAMES
# =====================================================

def normalize_skill(skill):

    skill = str(skill).lower().strip()
    skill = re.sub(r"\s+", " ", skill)

    aliases = {

        "powerbi": "power bi",

        "ms excel": "excel",
        "microsoft excel": "excel",
        "advanced excel": "excel",

        "postgres": "postgresql",

        "sklearn": "scikit-learn",

        "rest api": "rest apis",
        "rest api fundamentals": "rest apis",

        "efficientnet": "efficientnet-b0",

        "numpy library": "numpy",

        "joins": "join",
        "sql joins": "join",

        "pivot tables": "pivottables",
        "pivot table": "pivottables",

        "agile": "agile fundamentals",
        "agile fundamentals": "agile fundamentals"

    }

    return aliases.get(skill, skill)


# =====================================================
# 2. REMOVE DUPLICATE SKILLS
# =====================================================

def remove_duplicate_skills(skills):

    unique_skills = []
    seen_skills = set()

    for skill in skills:

        if not isinstance(skill, str):
            continue

        skill = skill.strip()

        if not skill:
            continue

        normalized = normalize_skill(skill)

        if normalized not in seen_skills:

            unique_skills.append(skill)
            seen_skills.add(normalized)

    return unique_skills


# =====================================================
# 3. FILTER UNWANTED SKILL ENTRIES
# =====================================================

def filter_skill_candidates(skills):

    filtered_skills = []

    section_headings = {

        "technical skills",
        "skills",
        "soft skills",
        "professional skills",
        "core competencies",
        "technical expertise",
        "areas of expertise",
        "key skills",
        "domain knowledge",
        "other skills",
        "certifications",
        "education",
        "experience",
        "projects"

    }

    unwanted_exact_terms = {

        "udemy",
        "oneroadmap",
        "sales",
        "purchase",
        "expense",
        "income",
        "customer type",
        "city",
        "date",
        "budget",
        "profit",
        "sub-category",
        "revenue",
        "product",
        "branch",
        "sales analysis",
        "customer",
        "top 5"

    }

    unwanted_keywords = [

        "certificate",
        "certification",
        "bootcamp",
        "training program",
        "complete mastery course"

    ]

    descriptive_keywords = [

        "application",
        "developed using",
        "built using",
        "implemented using",
        "project description",
        "python-based deep learning application"

    ]

    for skill in skills:

        if not isinstance(skill, str):
            continue

        skill = skill.strip()

        if not skill:
            continue

        normalized = skill.lower().strip()

        # Remove section headings
        if normalized in section_headings:
            continue

        # Remove irrelevant standalone terms
        if normalized in unwanted_exact_terms:
            continue

        # Remove certification and course names
        if any(
            keyword in normalized
            for keyword in unwanted_keywords
        ):
            continue

        if normalized.startswith("python for data science"):
            continue

        # Remove descriptive project phrases
        if any(
            keyword in normalized
            for keyword in descriptive_keywords
        ):
            continue

        # Remove long descriptive sentences
        if len(skill.split()) > 7:
            continue

        filtered_skills.append(skill)

    return remove_duplicate_skills(filtered_skills)


# =====================================================
# 4. TECHNICAL SKILLS
# =====================================================

TECHNICAL_SKILLS = {

    # Programming languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "sql",
    "r",

    # Frameworks and libraries
    "fastapi",
    "flask",
    "django",
    "react",
    "node.js",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "pytorch",
    "tensorflow",
    "keras",
    "torchvision",
    "opencv",
    "langchain",

    # Databases
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "oracle",

    # Analytics and BI
    "power bi",
    "power query",
    "excel",
    "dax",
    "tableau",
    "microsoft office",
    "jira",

    # Excel and reporting tools
    "pivottables",
    "lookups",
    "filters",
    "data summaries",

    # Cloud and DevOps
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "git",
    "github",
    "version control",

    # AI and ML
    "machine learning",
    "deep learning",
    "computer vision",
    "natural language processing",
    "efficientnet-b0",
    "ollama",
    "rag",
    "transfer learning",

    # APIs and data formats
    "rest apis",
    "json",
    "xml",

    # Data processing
    "data cleaning",
    "data transformation",
    "data visualization",
    "data analysis",
    "data validation",
    "data preprocessing",
    "data augmentation",
    "evaluation pipelines",
    "dashboard development",
    "data modeling",

    # SQL concepts
    "sql queries",
    "group by",
    "join",
    "aggregate functions",

    # ML evaluation concepts
    "accuracy",
    "precision",
    "recall",
    "confusion matrix"

}


# =====================================================
# 5. PROFESSIONAL SKILLS
# =====================================================

PROFESSIONAL_SKILLS = {

    "agile",
    "agile fundamentals",
    "ui/ux design",
    "user stories",
    "acceptance criteria",
    "requirement traceability",
    "as-is/to-be process analysis",
    "communication",
    "teamwork",
    "problem solving",
    "critical thinking",
    "project management",
    "leadership",
    "time management",
    "collaboration",
    "adaptability",
    "decision making",
    "stakeholder management"

}


# =====================================================
# 6. DOMAIN KNOWLEDGE
# =====================================================

DOMAIN_SKILLS = {

    # Business analysis
    "business analysis",
    "data analysis & reporting",
    "business reporting",
    "financial analysis",
    "financial reporting",
    "sales analysis",
    "purchase analysis",

    # MIS and operations
    "mis reports",
    "mis reporting",
    "management information systems",
    "operational reporting",

    # Financial operations
    "reconciliation",
    "consolidation",
    "financial data analysis",
    "expense management",
    "inventory management",

    # Business concepts
    "profitability analysis",
    "performance analysis",
    "kpi analysis",
    "trend analysis",
    "variance analysis"

}


# =====================================================
# 7. CLASSIFY SKILLS USING PYTHON
# =====================================================

def classify_skills_with_python(skills):

    cleaned_skills = filter_skill_candidates(skills)

    technical_skills = []
    professional_skills = []
    domain_skills = []
    other_skills = []

    for skill in cleaned_skills:

        normalized = normalize_skill(skill)

        if normalized in TECHNICAL_SKILLS:

            technical_skills.append(skill)

        elif normalized in PROFESSIONAL_SKILLS:

            professional_skills.append(skill)

        elif normalized in DOMAIN_SKILLS:

            domain_skills.append(skill)

        else:

            other_skills.append(skill)

    return {

        "technical_skills": technical_skills,

        "professional_skills": professional_skills,

        "domain_skills": domain_skills,

        "other_skills": other_skills

    }


# =====================================================
# 8. OPTIONAL AI-BASED TECHNICAL SKILL CLASSIFICATION
# =====================================================

def classify_technical_skills(skills):

    cleaned_skills = filter_skill_candidates(skills)

    if not cleaned_skills:
        return []

    prompt = f"""
    You are an expert technical skill classification system.

    Identify genuine technical skills from the input.

    INCLUDE:
    - Programming languages
    - Frameworks and libraries
    - Databases
    - Cloud technologies
    - Developer tools
    - Data analytics tools
    - Machine learning technologies
    - Deep learning technologies
    - API technologies
    - Testing tools
    - Technical data concepts

    EXCLUDE:
    - Certifications
    - Course names
    - Job titles
    - Soft skills
    - General business descriptions
    - Section headings
    - Long descriptive sentences

    RULES:
    1. Do not invent skills.
    2. Preserve original skill names.
    3. Return only skills present in the input.
    4. Return valid JSON only.

    INPUT:
    {json.dumps(cleaned_skills)}

    REQUIRED JSON:
    {{
        "technical_skills": []
    }}
    """

    try:

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format="json"
        )

        result = response["message"]["content"]

        if not result or not result.strip():
            raise ValueError("Empty response from Ollama")

        ai_result = json.loads(result)

        classified_skills = ai_result.get(
            "technical_skills",
            []
        )

        if not isinstance(classified_skills, list):
            raise ValueError("Technical skills must be a list")

        original_lookup = {
            normalize_skill(skill): skill
            for skill in cleaned_skills
        }

        verified_skills = []

        for skill in classified_skills:

            if not isinstance(skill, str):
                continue

            original_skill = original_lookup.get(
                normalize_skill(skill)
            )

            if original_skill:
                verified_skills.append(original_skill)

        return remove_duplicate_skills(verified_skills)

    except Exception as error:

        print("AI skill classification error:", error)

        return []


# =====================================================
# 9. VALIDATE EXPERIENCE
# =====================================================

def validate_experience(experience):

    issues = []

    if not isinstance(experience, list):

        return [
            "Experience information must be a list"
        ]

    for index, job in enumerate(experience):

        if not isinstance(job, dict):

            issues.append(
                f"Experience {index + 1}: Invalid experience entry"
            )

            continue

        if not job.get("job_title"):

            issues.append(
                f"Experience {index + 1}: Job title is missing"
            )

        if not job.get("company"):

            issues.append(
                f"Experience {index + 1}: Company is missing"
            )

        if not job.get("duration"):

            issues.append(
                f"Experience {index + 1}: Duration is missing"
            )

    return issues


# =====================================================
# 10. VALIDATE EDUCATION
# =====================================================

def validate_education(education):

    issues = []

    if not isinstance(education, list):

        return [
            "Education information must be a list"
        ]

    for index, degree in enumerate(education):

        if not isinstance(degree, dict):

            issues.append(
                f"Education {index + 1}: Invalid education entry"
            )

            continue

        if not degree.get("degree"):

            issues.append(
                f"Education {index + 1}: Degree is missing"
            )

        if not degree.get("institution"):

            issues.append(
                f"Education {index + 1}: Institution is missing"
            )

        if not degree.get("year"):

            issues.append(
                f"Education {index + 1}: Year is missing"
            )

    return issues


# =====================================================
# 11. VALIDATE COMPLETE RESUME
# =====================================================

def validate_resume(resume_details):

    issues = []

    if not isinstance(resume_details, dict):

        return ["Invalid resume information"]

    experience = resume_details.get(
        "experience",
        []
    )

    education = resume_details.get(
        "education",
        []
    )

    issues.extend(
        validate_experience(experience)
    )

    issues.extend(
        validate_education(education)
    )

    return issues


# =====================================================
# 12. TEST RESUME VALIDATOR
# =====================================================

if __name__ == "__main__":

    skills = [

        "Python",
        "SQL",
        "Technical Skills",
        "Power BI",
        "PowerBI",
        "Python for Data Science Pro",
        "Pandas",
        "Machine Learning",
        "Data Analyst Certificate",
        "PyTorch",
        "NumPy",
        "FastAPI",
        "REST API Fundamentals",
        "PostgreSQL",
        "Advanced Excel",
        "Microsoft Excel",
        "Power Query",
        "DAX",

        "Agile Fundamentals",
        "User Stories",
        "Acceptance Criteria",
        "UI/UX Design",
        "Communication",

        "Business Analysis",
        "Data Analysis & Reporting",
        "Dashboard Development",
        "Microsoft Office",
        "Jira",
        "Data Modeling",
        "Reconciliation",
        "PivotTables",
        "Lookups",
        "Filters",
        "SQL Queries",
        "GROUP BY",
        "JOINS",
        "Aggregate Functions",
        "Accuracy",
        "Precision",
        "Recall",
        "Confusion Matrix",
        "Version Control",
        "MIS Reports",

        "Revenue",
        "Customer Type",
        "City",
        "Date",
        "Budget",
        "Profit",
        "Udemy",
        "OneRoadMap"

    ]

    print("\n========== ORIGINAL SKILLS ==========")
    print(skills)

    classification = classify_skills_with_python(skills)

    print("\n========== FINAL CLASSIFICATION ==========")

    print(
        json.dumps(
            classification,
            indent=4
        )
    )

    print("\n========== AI CLASSIFICATION ==========")

    ai_result = classify_technical_skills(skills)

    print(ai_result)
