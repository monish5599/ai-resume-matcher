
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Form
)

import fitz

from app.resume_parser import extract_text_from_pdf
from app.resume_extractor import extract_resume_details
from app.jd_extractor import extract_job_details
from app.matching_engine import match_resume_with_job
from app.skill_gap_analyzer import analyze_skill_gaps


# =====================================================
# INITIALIZE FASTAPI
# =====================================================

app = FastAPI(
    title="AI Resume Matcher",
    description="AI-powered Resume Analysis and Job Matching API",
    version="1.0.0"
)


# =====================================================
# VALIDATE AND EXTRACT PDF
# =====================================================

async def process_resume_pdf(file: UploadFile):

    # Check file extension
    if not file.filename or not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file"
        )

    # Read uploaded file
    pdf_file = await file.read()

    if not pdf_file:

        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty"
        )

    try:

        extracted_text = extract_text_from_pdf(pdf_file)

    except (fitz.FileDataError, fitz.EmptyFileError):

        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file"
        )

    if not extracted_text.strip():

        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF"
        )

    return extracted_text


# =====================================================
# HOME ROUTE
# =====================================================

@app.get("/")
def home():

    return {
        "message": "AI Resume Matcher API is running",
        "version": "1.0.0"
    }


# =====================================================
# RESUME UPLOAD API
# =====================================================

@app.post("/resumes/upload")
async def upload_resume(
    file: UploadFile = File(...)
):

    # 1. Extract resume text
    extracted_text = await process_resume_pdf(file)

    # 2. Extract resume information
    resume_details = extract_resume_details(
        extracted_text
    )

    # 3. Return response
    return {

        "filename": file.filename,

        "resume_details": resume_details

    }


# =====================================================
# JOB MATCHING API
# =====================================================

@app.post("/jobs/match")
async def match_job(

    file: UploadFile = File(...),

    job_description: str = Form(...)

):

    # 1. Validate job description
    if not job_description.strip():

        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty"
        )

    # 2. Extract resume text
    resume_text = await process_resume_pdf(file)

    # 3. Extract resume information
    resume_details = extract_resume_details(
        resume_text
    )

    # 4. Extract job description information
    job_details = extract_job_details(
        job_description
    )

    # 5. Match resume with job requirements
    matching_result = match_resume_with_job(
        resume_details.get("skills", []),
        job_details
    )

    # 6. Analyze skill gaps
    skill_gap_result = analyze_skill_gaps(
        matching_result
    )

    # 7. Return complete analysis
    return {

        "resume_details": resume_details,

        "job_details": job_details,

        "matching_result": matching_result,

        "skill_gap_analysis": skill_gap_result

    }
