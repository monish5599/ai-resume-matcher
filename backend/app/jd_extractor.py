
import ollama
import json

def extract_job_details(job_description):

    prompt = f"""
    You are an expert job description analyzer.

    Analyze the complete job description.

    Extract the following information:

    1. Job title
    2. Required technical and professional skills
    3. Preferred or optional skills
    4. Years of experience, if mentioned
    5. Educational qualifications, if mentioned

    Instructions:

    - Read the entire job description.
    - Identify all relevant skills.
    - Do not restrict yourself to a predefined skill list.
    - Do not invent information.
    - If information is unavailable, return null.
    - Avoid duplicate skills.
    - Separate required skills from preferred skills.

    Return only valid JSON in this format:

    {{
        "job_title": "Python Developer",
        "required_skills": ["Python", "SQL"],
        "preferred_skills": ["FastAPI", "Machine Learning"],
        "experience": "1-2 years",
        "education": "Bachelor's degree"
    }}

    Job Description:
    {job_description}
    """

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

    return json.loads(result)

