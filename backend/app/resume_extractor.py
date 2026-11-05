import json
import re
import ollama

from app.resume_validator import (
    remove_duplicate_skills,
    validate_resume,
    classify_skills_with_python,
)


# =====================================================
# 1. EXTRACT EMAIL
# =====================================================

def extract_email(text):
    emails = re.findall(r"[\w.+-]+@[\w.-]+\.\w+", text)
    return emails[0] if emails else None


# =====================================================
# 2. EXTRACT PHONE NUMBER
# =====================================================

def extract_phone(text):
    pattern = r"(?<!\d)(?:\+?91[\s-]?)?[6-9]\d{9}(?!\d)"
    phones = re.findall(pattern, text)
    return phones[0].strip() if phones else None


# =====================================================
# 3. EXTRACT DATE RANGES
# =====================================================

def extract_date_ranges(text):
    """Extract common numeric month/year date ranges."""
    pattern = (
        r"\b(?:0?[1-9]|1[0-2])[/.-]\d{4}"
        r"\s*(?:-|to|–|—)\s*"
        r"(?:0?[1-9]|1[0-2])[/.-]\d{4}|"
        r"\b(?:0?[1-9]|1[0-2])[/.-]\d{4}"
        r"\s*(?:-|to|–|—)\s*(?:Present|Current)\b"
    )
    return re.findall(pattern, text, re.IGNORECASE)


# =====================================================
# 4. EXTRACT NAME
# =====================================================

def extract_name(text):
    lines = text.splitlines()

    ignored_titles = {
        "python developer",
        "data analyst",
        "software engineer",
        "ai engineer",
        "machine learning engineer",
    }

    for line in lines[:10]:
        line = line.strip()

        if not line:
            continue
        if "@" in line or "linkedin.com" in line.lower():
            continue
        if any(char.isdigit() for char in line):
            continue
        if len(line.split()) > 4:
            continue
        if line.lower() in ignored_titles:
            continue

        return line

    return None


# =====================================================
# 5. EXTRACT TECHNICAL SKILLS
# =====================================================

def extract_skills_from_resume_text(text):
    technical_skills = [
        # Programming languages
        "Python", "Java", "JavaScript", "C++", "C#", "SQL",

        # Analytics and BI
        "Power BI", "Power Query", "Microsoft Excel",
        "Advanced Excel", "Excel", "Tableau", "DAX",

        # Python libraries
        "Pandas", "NumPy", "Matplotlib", "Seaborn", "Scikit-learn",

        # Machine learning and deep learning
        "Machine Learning", "Deep Learning", "PyTorch",
        "TensorFlow", "Keras", "Torchvision", "EfficientNet-B0",
        "EfficientNet", "Computer Vision",
        "Natural Language Processing", "Transfer Learning",

        # Backend and APIs
        "FastAPI", "Flask", "Django", "REST APIs",
        "REST API", "REST API Fundamentals", "JSON",

        # Databases
        "PostgreSQL", "MySQL", "MongoDB", "SQLite", "Oracle",

        # Cloud and developer tools
        "Git", "GitHub", "Docker", "Kubernetes", "Azure",
        "AWS", "Ollama", "LangChain",

        # Data processing
        "Data Cleaning", "Data Transformation", "Data Visualization",
        "Data Analysis", "Data Validation", "Data Preprocessing",
        "Data Augmentation", "Evaluation Pipelines",

        # AI technologies
        "RAG", "OpenCV",

        # SQL and analytics concepts
        "SQL Queries", "GROUP BY", "JOINS", "JOIN",
        "Aggregate Functions", "PivotTables", "Lookups", "Filters",

        # Model evaluation
        "Accuracy", "Precision", "Recall", "Confusion Matrix",

        # Development practices
        "Version Control",
    ]

    found_skills = []

    for skill in technical_skills:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return remove_duplicate_skills(found_skills)


# =====================================================
# 6. EXTRACT PROFESSIONAL SKILLS
# =====================================================

def extract_professional_skills_from_text(text):
    professional_skills = [
        "Agile",
        "Agile Fundamentals",
        "User Stories",
        "Acceptance Criteria",
        "Requirement Traceability",
        "As-Is/To-Be Process Analysis",
        "UI/UX Design",
        "Communication",
        "Teamwork",
        "Problem Solving",
        "Critical Thinking",
        "Project Management",
        "Leadership",
        "Time Management",
        "Collaboration",
        "Adaptability",
        "Decision Making",
        "Stakeholder Management",
    ]

    found_skills = []

    for skill in professional_skills:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return remove_duplicate_skills(found_skills)


# =====================================================
# 7. EXTRACT DOMAIN SKILLS
# =====================================================

def extract_domain_skills_from_text(text):
    domain_skills = [
        "Business Analysis",
        "Data Analysis & Reporting",
        "Business Reporting",
        "Financial Analysis",
        "Financial Reporting",
        "Sales Analysis",
        "Purchase Analysis",
        "MIS Reports",
        "MIS Reporting",
        "Management Information Systems",
        "Operational Reporting",
        "Reconciliation",
        "Consolidation",
        "Financial Data Analysis",
        "Expense Management",
        "Inventory Management",
        "Profitability Analysis",
        "Performance Analysis",
        "KPI Analysis",
        "Trend Analysis",
        "Variance Analysis",
    ]

    found_skills = []

    for skill in domain_skills:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return remove_duplicate_skills(found_skills)


# =====================================================
# 8. PYTHON FALLBACK FOR PROJECT EXTRACTION
# =====================================================

def extract_projects_with_python(text):
    """
    Basic fallback project extractor.
    It looks for a PROJECTS section and uses short, non-bullet
    lines as possible project names. It does not invent details.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    section_start = None
    section_end = len(lines)

    project_heading = re.compile(
        r"^(projects?|academic projects?|personal projects?)\s*:?\s*$",
        re.IGNORECASE,
    )
    next_section = re.compile(
        r"^(education|experience|work experience|employment|"
        r"skills|technical skills|certifications?|achievements?|"
        r"professional skills|domain skills|summary|"
        r"declaration|languages)\s*:?\s*$",
        re.IGNORECASE,
    )

    for index, line in enumerate(lines):
        if project_heading.match(line):
            section_start = index + 1
            break

    if section_start is None:
        return []

    for index in range(section_start, len(lines)):
        if next_section.match(lines[index]):
            section_end = index
            break

    project_lines = lines[section_start:section_end]
    projects = []
    current_project = None

    for line in project_lines:
        cleaned = re.sub(r"^[\-\*\•\d\.\)\s]+", "", line).strip()
        if not cleaned:
            continue

        # A short standalone line is treated as a possible project title.
        # Avoid interpreting obvious technology/description lines as titles.
        looks_like_title = (
            len(cleaned) <= 90
            and not re.search(r"[:;]$", cleaned)
            and not re.search(
                r"\b(developed|built|created|implemented|using|technologies|"
                r"technology|tools|responsible|worked|designed)\b",
                cleaned,
                re.IGNORECASE,
            )
        )

        if looks_like_title:
            if current_project:
                projects.append(current_project)

            current_project = {
                "project_name": cleaned,
                "description": None,
                "technologies": [],
            }
        elif current_project:
            if current_project["description"]:
                current_project["description"] += " " + cleaned
            else:
                current_project["description"] = cleaned

    if current_project:
        projects.append(current_project)

    # Keep only projects that have a meaningful name.
    return [
        project for project in projects
        if project.get("project_name")
    ]


# =====================================================
# 9. EXTRACT RESUME INFORMATION USING OLLAMA AI
# =====================================================

def extract_resume_information_with_ai(text):
    prompt = f"""
You are an accurate resume information extraction system.

Read the complete resume and extract only information explicitly
present in the resume. Do not guess, assume, or invent information.

Return ONLY one valid JSON object. Do not use Markdown code fences.

Extract these sections:
1. Technical skills
2. Education
3. Work experience
4. Projects
5. Certifications

SKILL RULES:
- Extract programming languages, frameworks, libraries, databases,
  cloud technologies, analytics tools, and AI/ML technologies.
- Include technical skills explicitly mentioned in project descriptions
  and work experience.
- Do not include section headings as skills.
- Do not invent skills.

EDUCATION RULES:
- Extract degree, institution, and dates/year exactly as written.
- Do not invent missing details.

EXPERIENCE RULES:
- Extract every job separately.
- Extract job title, company, duration, and a concise description.
- Preserve dates as written.
- Do not confuse project dates with employment dates.
- If a field is unavailable, use null.

IMPORTANT PROJECT EXTRACTION RULES:
- Carefully locate the section titled PROJECTS, PROJECT, ACADEMIC PROJECTS,
  or PERSONAL PROJECTS.
- Extract EVERY individual project listed in that section.
- A project title may be a short standalone line followed by one or more
  description lines.
- Do not mistake the word PROJECTS itself for a project.
- For every project, extract its actual title, description, and technologies.
- Technologies may appear after labels such as Technologies, Tech Stack,
  Tools Used, or may be mentioned in the description.
- Preserve the project name as written.
- Do not combine separate projects into one project.
- Do not create a placeholder project if no project is present.
- If a project name is present but its description is absent, use null
  for description.
- If technologies are absent, use an empty list.
- Do not invent project names, descriptions, or technologies.

CERTIFICATION RULES:
- Extract certification name, provider, and date if present.
- Do not add certification names as technical skills.
- Do not invent certifications.

EMPTY SECTION RULES:
- If no education is found, return education as [].
- If no experience is found, return experience as [].
- If no projects are found, return projects as [].
- If no certifications are found, return certifications as [].
- Never return placeholder objects with all fields null.

REQUIRED JSON STRUCTURE:
{{
  "skills": [],
  "education": [
    {{
      "degree": null,
      "institution": null,
      "year": null
    }}
  ],
  "experience": [
    {{
      "job_title": null,
      "company": null,
      "duration": null,
      "description": null
    }}
  ],
  "projects": [
    {{
      "project_name": null,
      "description": null,
      "technologies": []
    }}
  ],
  "certifications": [
    {{
      "name": null,
      "provider": null,
      "date": null
    }}
  ]
}}

For missing sections, return an empty list.
For missing individual fields, return null.
Do not return placeholder objects.

RESUME TEXT:
{text}
"""

    try:
        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            format="json",
        )

        if hasattr(response, "message"):
            result = response.message.content
        else:
            result = response.get("message", {}).get("content", "")

        print("\n========== OLLAMA RESPONSE ==========")
        print(response)
        print("\n========== AI CONTENT ==========")
        print(repr(result))

        if not result or not result.strip():
            raise ValueError("Ollama returned an empty response")

        ai_result = json.loads(result)

        if not isinstance(ai_result, dict):
            raise ValueError("AI response must be a JSON object")

        for key in (
            "skills",
            "education",
            "experience",
            "projects",
            "certifications",
        ):
            if not isinstance(ai_result.get(key), list):
                ai_result[key] = []

        # Remove empty placeholder project objects from the AI output.
        ai_result["projects"] = [
            project for project in ai_result["projects"]
            if isinstance(project, dict)
            and (
                project.get("project_name")
                or project.get("description")
                or project.get("technologies")
            )
        ]

        print("\nJSON extraction successful!")
        return ai_result

    except json.JSONDecodeError as error:
        print("Invalid JSON response from Ollama")
        raise ValueError(
            "AI returned an invalid JSON response"
        ) from error

    except Exception as error:
        print("\nResume extraction error:", error)
        raise


# =====================================================
# 10. EXTRACT COMPLETE RESUME DETAILS
# =====================================================

def extract_resume_details(text):

    # A. Extract structured information using AI
    ai_result = extract_resume_information_with_ai(text)

    # B. Extract AI skills safely
    ai_skills = ai_result.get("skills", [])

    if not isinstance(ai_skills, list):
        ai_skills = []

    ai_skills = [
        skill for skill in ai_skills
        if isinstance(skill, str)
    ]

    # C. Extract skills using Python
    text_skills = extract_skills_from_resume_text(text)
    professional_text_skills = extract_professional_skills_from_text(text)
    domain_text_skills = extract_domain_skills_from_text(text)

    # D. Prepare project details from AI
    projects = ai_result.get("projects", [])

    if not isinstance(projects, list):
        projects = []

    # E. If AI misses projects, try the Python fallback
    if not projects:
        print("\nAI did not extract projects. Trying Python fallback...")
        projects = extract_projects_with_python(text)

    project_skills = []
    valid_projects = []

    for project in projects:
        if not isinstance(project, dict):
            continue

        project_name = project.get("project_name")
        description = project.get("description") or ""

        if not isinstance(project_name, str):
            project_name = None

        if not isinstance(description, str):
            description = ""

        technologies = project.get("technologies", [])

        if not isinstance(technologies, list):
            technologies = []

        technologies = [
            item for item in technologies
            if isinstance(item, str)
        ]

        # Extract technologies from project title and description too.
        project_source_text = " ".join(
            part for part in [project_name or "", description] if part
        )
        description_skills = extract_skills_from_resume_text(
            project_source_text
        )

        combined_technologies = remove_duplicate_skills(
            technologies + description_skills
        )

        # Ignore empty placeholder projects.
        if not project_name and not description and not combined_technologies:
            continue

        project["project_name"] = project_name
        project["description"] = description or None
        project["technologies"] = combined_technologies

        project_skills.extend(combined_technologies)
        valid_projects.append(project)

    projects = valid_projects

    # F. Combine all skill sources
    all_skills = (
        ai_skills
        + text_skills
        + project_skills
        + professional_text_skills
        + domain_text_skills
    )

    # G. Remove duplicate skills
    unique_skills = remove_duplicate_skills(all_skills)

    # H. Classify into four categories
    skill_classification = classify_skills_with_python(unique_skills)

    final_skills = skill_classification.get("technical_skills", [])
    professional_skills = skill_classification.get("professional_skills", [])
    domain_skills = skill_classification.get("domain_skills", [])
    other_skills = skill_classification.get("other_skills", [])

    # I. Prepare education, experience and certifications
    education = ai_result.get("education", [])
    experience = ai_result.get("experience", [])
    certifications = ai_result.get("certifications", [])

    if not isinstance(education, list):
        education = []
    if not isinstance(experience, list):
        experience = []
    if not isinstance(certifications, list):
        certifications = []

    # J. Filter unsupported certification names.
    # This confirms the name appears in the resume text; it does not
    # independently authenticate that the certificate is genuine.
    verified_certifications = []

    for certification in certifications:
        if not isinstance(certification, dict):
            continue

        name = certification.get("name")

        if (
            isinstance(name, str)
            and name.strip()
            and name.casefold() in text.casefold()
        ):
            verified_certifications.append(certification)

    certifications = verified_certifications

    # K. Prepare final resume details
    resume_details = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": final_skills,
        "professional_skills": professional_skills,
        "domain_skills": domain_skills,
        "other_skills": other_skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    }

    # L. Validate resume
    validation_issues = validate_resume(resume_details)
    resume_details["validation_issues"] = validation_issues

    return resume_details


# =====================================================
# 11. TEST RESUME EXTRACTION
# =====================================================

if __name__ == "__main__":

    sample_resume = """
    V. MONISH

    Email: monish@gmail.com
    Phone: 9884569131

    EDUCATION:
    BE Computer Science and Engineering
    Sathyabama University
    2025

    EXPERIENCE:
    Data Analyst Intern
    Jeanuvs Pvt Ltd
    07/2025 - 09/2025
    Worked with Power BI and financial data.

    PROJECTS:

    AI Resume Matcher
    Built using Python, FastAPI and Ollama.

    Skin Disease Classification
    Developed using PyTorch, Torchvision,
    EfficientNet-B0 and Scikit-learn.

    SKILLS:
    Python, SQL, Power BI, Machine Learning,
    Pandas, NumPy, FastAPI

    PROFESSIONAL SKILLS:
    Agile Fundamentals, User Stories,
    Acceptance Criteria

    DOMAIN SKILLS:
    Business Analysis, Data Analysis & Reporting,
    MIS Reports, Reconciliation

    CERTIFICATIONS:
    Python Programming
    """

    result = extract_resume_details(sample_resume)

    print("\n========== FINAL RESUME DETAILS ==========")
    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        )
    )
