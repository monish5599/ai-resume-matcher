import json
import re


# =====================================================
# 1. NORMALIZE SKILLS
# =====================================================

def normalize_skill(skill):

    skill = str(skill).lower().strip()

    # Normalize spaces
    skill = re.sub(r"\s+", " ", skill)

    # Normalize spaces around slash
    skill = re.sub(r"\s*/\s*", "/", skill)

    skill_aliases = {

        "postgres": "postgresql",
        "postgresql": "postgresql",

        "powerbi": "power bi",
        "power bi": "power bi",

        "ms excel": "excel",
        "microsoft excel": "excel",

        "rest api": "rest apis",
        "rest api fundamentals": "rest apis",
        "rest apis": "rest apis",

        "py": "python",

        "sklearn": "scikit-learn",

        "pytorch/tensorflow": "pytorch/tensorflow",
        "pytorch or tensorflow": "pytorch or tensorflow",
        "pytorch/tensorflow/keras": "pytorch/tensorflow/keras"

    }

    return skill_aliases.get(skill, skill)


# =====================================================
# 2. ALTERNATIVE REQUIREMENTS
# =====================================================
# Any one of these skills can satisfy the requirement.

REQUIREMENT_ALTERNATIVES = {

    "pytorch/tensorflow": [
        "pytorch",
        "tensorflow"
    ],

    "pytorch or tensorflow": [
        "pytorch",
        "tensorflow"
    ],

    "pytorch/tensorflow/keras": [
        "pytorch",
        "tensorflow",
        "keras"
    ]

}


# =====================================================
# 3. RELATED SKILLS
# =====================================================
# Related skills receive partial credit.
# They are not treated as exact equivalents.

RELATED_SKILLS = {

    "deep learning": [
        "pytorch",
        "tensorflow",
        "keras"
    ],

    "machine learning": [
        "scikit-learn",
        "xgboost"
    ],

    "data analysis": [
        "pandas",
        "numpy"
    ]

}


# =====================================================
# 4. PREPARE RESUME SKILLS
# =====================================================

def prepare_resume_skills(resume_skills):

    normalized_skills = []
    seen_skills = set()

    for skill in resume_skills:

        if not isinstance(skill, str):
            continue

        skill = skill.strip()

        if not skill:
            continue

        normalized = normalize_skill(skill)

        if normalized not in seen_skills:

            normalized_skills.append({
                "original": skill,
                "normalized": normalized
            })

            seen_skills.add(normalized)

    return normalized_skills


# =====================================================
# 5. REMOVE DUPLICATE JOB REQUIREMENTS
# =====================================================

def prepare_job_requirements(skills):

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

            unique_skills.append({
                "original": skill,
                "normalized": normalized
            })

            seen_skills.add(normalized)

    return unique_skills


# =====================================================
# 6. FIND RELATED SKILLS
# =====================================================

def find_related_skills(
    available_resume_skills,
    required_skill
):

    related_skills = RELATED_SKILLS.get(
        normalize_skill(required_skill),
        []
    )

    matched_related = []

    for resume_skill in available_resume_skills:

        if resume_skill["normalized"] in [
            normalize_skill(skill)
            for skill in related_skills
        ]:

            matched_related.append(
                resume_skill["original"]
            )

    return matched_related


# =====================================================
# 7. FIND ALTERNATIVE MATCH
# =====================================================

def find_alternative_match(
    available_resume_skills,
    required_skill
):

    alternatives = REQUIREMENT_ALTERNATIVES.get(
        normalize_skill(required_skill),
        []
    )

    for alternative in alternatives:

        normalized_alternative = normalize_skill(
            alternative
        )

        for resume_skill in available_resume_skills:

            if resume_skill["normalized"] == normalized_alternative:

                return resume_skill["original"]

    return None


# =====================================================
# 8. MATCH RESUME WITH JOB DESCRIPTION
# =====================================================

def match_resume_with_job(resume_skills, job_details):

    # Prepare resume skills
    prepared_resume_skills = prepare_resume_skills(
        resume_skills
    )

    # Prepare job requirements
    required_skills = prepare_job_requirements(
        job_details.get("required_skills", [])
    )

    preferred_skills = prepare_job_requirements(
        job_details.get("preferred_skills", [])
    )

    # Track skills already used for required matches
    used_resume_skills = set()

    matched_required = []
    alternative_matches = {}
    related_matches = {}
    missing_required = []

    # -------------------------------------------------
    # PASS 1: EXACT MATCHING
    # -------------------------------------------------

    for requirement in required_skills:

        required_name = requirement["original"]
        normalized_required = requirement["normalized"]

        for resume_skill in prepared_resume_skills:

            if (
                resume_skill["normalized"] == normalized_required
                and resume_skill["normalized"] not in used_resume_skills
            ):

                matched_required.append(required_name)

                used_resume_skills.add(
                    resume_skill["normalized"]
                )

                break

    # -------------------------------------------------
    # PASS 2: ALTERNATIVE MATCHING
    # -------------------------------------------------

    for requirement in required_skills:

        required_name = requirement["original"]

        if required_name in matched_required:
            continue

        available_skills = [
            skill for skill in prepared_resume_skills
            if skill["normalized"] not in used_resume_skills
        ]

        alternative = find_alternative_match(
            available_skills,
            required_name
        )

        if alternative:

            matched_required.append(required_name)

            alternative_matches[required_name] = alternative

            used_resume_skills.add(
                normalize_skill(alternative)
            )

    # -------------------------------------------------
    # PASS 3: RELATED SKILL MATCHING
    # -------------------------------------------------

    for requirement in required_skills:

        required_name = requirement["original"]

        if required_name in matched_required:
            continue

        available_skills = [
            skill for skill in prepared_resume_skills
            if skill["normalized"] not in used_resume_skills
        ]

        related = find_related_skills(
            available_skills,
            required_name
        )

        if related:

            related_matches[required_name] = related

            for skill in related:

                used_resume_skills.add(
                    normalize_skill(skill)
                )

    # -------------------------------------------------
    # PASS 4: FIND MISSING SKILLS
    # -------------------------------------------------

    matched_names = set(matched_required)
    matched_names.update(related_matches.keys())

    for requirement in required_skills:

        required_name = requirement["original"]

        if required_name not in matched_names:

            missing_required.append(required_name)

    # -------------------------------------------------
    # PASS 5: PREFERRED SKILLS
    # -------------------------------------------------

    matched_preferred = []

    resume_skill_set = {
        skill["normalized"]
        for skill in prepared_resume_skills
    }

    for skill in preferred_skills:

        if skill["normalized"] in resume_skill_set:

            matched_preferred.append(
                skill["original"]
            )

    # -------------------------------------------------
    # PASS 6: CALCULATE MATCH PERCENTAGE
    # -------------------------------------------------

    exact_count = (
        len(matched_required)
        - len(alternative_matches)
    )

    alternative_count = len(alternative_matches)

    related_count = len(related_matches)

    total_required = len(required_skills)

    # Scoring:
    # Exact match       = 1 point
    # Alternative match = 1 point
    # Related match     = 0.5 point
    # Missing skill     = 0 points

    score = (
        exact_count
        + alternative_count
        + (related_count * 0.5)
    )

    if total_required > 0:

        match_percentage = (
            score / total_required
        ) * 100

    else:

        match_percentage = 0

    # -------------------------------------------------
    # FINAL RESULT
    # -------------------------------------------------

    return {

        "match_percentage": round(
            match_percentage,
            2
        ),

        "total_required_skills": total_required,

        "match_breakdown": {

            "exact_matches": exact_count,

            "alternative_matches": alternative_count,

            "related_matches": related_count,

            "missing_skills": len(missing_required)

        },

        "matched_required_skills": sorted(
            matched_required
        ),

        "alternative_matches": alternative_matches,

        "related_matches": related_matches,

        "missing_required_skills": sorted(
            missing_required
        ),

        "matched_preferred_skills": sorted(
            matched_preferred
        )

    }


# =====================================================
# 9. TEST MATCHING ENGINE
# =====================================================

if __name__ == "__main__":

    resume_skills = [

        "Python",
        "Postgres",
        "PowerBI",
        "Excel",
        "PyTorch",
        "Pandas",
        "REST API Fundamentals"

    ]

    job_details = {

        "required_skills": [

            "Python",
            "PostgreSQL",
            "Power BI",
            "SQL",
            "Deep Learning",
            "REST APIs",
            "PyTorch/TensorFlow"

        ],

        "preferred_skills": [

            "Excel"

        ]

    }

    result = match_resume_with_job(
        resume_skills,
        job_details
    )

    print("\n========== RESUME MATCHING RESULT ==========")

    print(
        json.dumps(
            result,
            indent=4
        )
    )
