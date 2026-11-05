
# =====================================================
# SKILL GAP ANALYZER
# =====================================================


def analyze_skill_gaps(matching_result):

    # -------------------------------------------------
    # 1. GET MATCHING ENGINE RESULTS
    # -------------------------------------------------

    matched_required = matching_result.get(
        "matched_required_skills", []
    )

    alternative_matches = matching_result.get(
        "alternative_matches", {}
    )

    related_matches = matching_result.get(
        "related_matches", {}
    )

    missing_skills = matching_result.get(
        "missing_required_skills", []
    )

    preferred_matches = matching_result.get(
        "matched_preferred_skills", []
    )

    match_percentage = matching_result.get(
        "match_percentage", 0
    )

    match_breakdown = matching_result.get(
        "match_breakdown", {}
    )

    # -------------------------------------------------
    # 2. IDENTIFY EXACT MATCHES
    # -------------------------------------------------

    alternative_requirement_names = set(
        alternative_matches.keys()
    )

    exact_matches = [
        skill
        for skill in matched_required
        if skill not in alternative_requirement_names
    ]

    # -------------------------------------------------
    # 3. IDENTIFY ALTERNATIVE MATCHES
    # -------------------------------------------------

    alternative_match_details = []

    for required_skill, available_skill in alternative_matches.items():

        alternative_match_details.append({

            "required_skill": required_skill,

            "available_skill": available_skill,

            "status": "Alternative Match",

            "message": (
                f"{available_skill} satisfies the "
                f"{required_skill} requirement."
            )

        })

    # -------------------------------------------------
    # 4. IDENTIFY PARTIALLY MATCHED SKILLS
    # -------------------------------------------------

    improvement_skills = []

    for required_skill, related in related_matches.items():

        improvement_skills.append({

            "required_skill": required_skill,

            "available_related_skills": related,

            "status": "Partially Matched"

        })

    # -------------------------------------------------
    # 5. IDENTIFY MISSING SKILLS
    # -------------------------------------------------

    missing_skill_details = []

    for skill in missing_skills:

        missing_skill_details.append({

            "skill": skill,

            "status": "Missing"

        })

    # -------------------------------------------------
    # 6. IDENTIFY PREFERRED SKILLS
    # -------------------------------------------------

    preferred_skill_details = []

    for skill in preferred_matches:

        preferred_skill_details.append({

            "skill": skill,

            "status": "Preferred Skill Matched"

        })

    # -------------------------------------------------
    # 7. GENERATE LEARNING RECOMMENDATIONS
    # -------------------------------------------------

    recommendations = []

    # Recommendations for missing skills
    for skill in missing_skills:

        recommendations.append({

            "skill": skill,

            "priority": "High",

            "recommendation": (
                f"Learn and practice {skill}. "
                f"Build a practical project to demonstrate "
                f"your knowledge."
            )

        })

    # Recommendations for partially matched skills
    for item in improvement_skills:

        related_skills = ", ".join(
            item["available_related_skills"]
        )

        recommendations.append({

            "skill": item["required_skill"],

            "priority": "Medium",

            "recommendation": (
                f"Strengthen your knowledge of "
                f"{item['required_skill']} using your "
                f"existing experience with {related_skills}."
            )

        })

    # -------------------------------------------------
    # 8. PREPARE FINAL RESULT
    # -------------------------------------------------

    return {

        "match_percentage": match_percentage,

        "match_breakdown": match_breakdown,

        "exact_matches": exact_matches,

        "alternative_matches": alternative_match_details,

        "partially_matched_skills": improvement_skills,

        "missing_skills": missing_skill_details,

        "preferred_matches": preferred_skill_details,

        "recommendations": recommendations

    }


# =====================================================
# TEST SKILL GAP ANALYZER
# =====================================================

if __name__ == "__main__":

    import json

    matching_result = {

        "match_percentage": 71.43,

        "total_required_skills": 7,

        "match_breakdown": {

            "exact_matches": 4,

            "alternative_matches": 1,

            "related_matches": 0,

            "missing_skills": 2

        },

        "matched_required_skills": [

            "PostgreSQL",
            "Power BI",
            "PyTorch/TensorFlow",
            "Python",
            "REST APIs"

        ],

        "alternative_matches": {

            "PyTorch/TensorFlow": "PyTorch"

        },

        "related_matches": {},

        "missing_required_skills": [

            "Deep Learning",
            "SQL"

        ],

        "matched_preferred_skills": [

            "Excel"

        ]

    }

    result = analyze_skill_gaps(matching_result)

    print("\n========== SKILL GAP ANALYSIS ==========")

    print(
        json.dumps(
            result,
            indent=4
        )
    )
