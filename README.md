# AI Resume Matcher

An AI-powered Resume Analysis and Job Matching application built using Python, FastAPI, Flask, and Ollama. The application extracts information from resumes, analyzes job descriptions, compares technical skills, identifies skill gaps, and provides recommendations to help candidates improve their job readiness.

## 1. Project Overview

Finding out whether a resume matches a job description can be time-consuming. Candidates often struggle to identify missing skills and understand how well their experience aligns with job requirements.

AI Resume Matcher helps automate this process by analyzing PDF resumes and job descriptions using a locally running Large Language Model (LLM).

The application generates a resume analysis report containing extracted candidate information, matched skills, missing skills, a match percentage, and skill gap recommendations.

## 2. Problem Statement

Job seekers often face challenges such as:

- Identifying relevant skills from their resumes.
- Understanding job description requirements.
- Finding missing technical skills.
- Evaluating their resume against a specific job role.
- Identifying areas for professional improvement.

This project aims to simplify resume evaluation through AI-powered information extraction and skill matching.

## 3. Key Features

- PDF Resume Parsing: Extracts text from uploaded PDF resumes.
- AI Resume Information Extraction: Extracts candidate details, education, experience, projects, certifications, and skills.
- Job Description Analysis: Identifies job titles, required skills, preferred skills, experience, and education requirements.
- Skill Classification: Organizes extracted skills into technical, professional, and domain-related categories.
- Resume Matching: Compares candidate skills with job requirements.
- Skill Gap Analysis: Identifies missing and related skills.
- Match Percentage: Calculates a skill-based compatibility score.
- AI Recommendations: Provides suggestions for improving missing skills.
- Interactive Dashboard: Displays analysis results through a user-friendly interface.
- Local LLM Integration: Uses Ollama to run the language model locally.

## 4. Technology Stack

| Category                | Technologies          |
| ----------------------- | --------------------- |
| Programming Language    | Python                |
| Backend Framework       | FastAPI               |
| Frontend Framework      | Flask                 |
| AI / LLM                | Ollama                |
| Language Model          | Qwen 2.5 3B           |
| PDF Processing          | PyMuPDF               |
| Data Validation         | Pydantic              |
| API Communication       | REST API, JSON        |
| HTTP Requests           | Requests              |
| Frontend                | HTML, CSS, JavaScript |
| Development Environment | VS Code               |

## 5. System Architecture

The application follows a frontend-backend architecture.

1. The user uploads a PDF resume and enters a job description through the Flask frontend.
2. Flask sends the resume and job description to the FastAPI backend.
3. PyMuPDF extracts text from the uploaded PDF.
4. Ollama with Qwen 2.5 3B extracts structured information from the resume and job description.
5. Python-based modules classify skills, compare requirements, and calculate the match percentage.
6. The skill gap analyzer generates recommendations.
7. FastAPI returns the analysis as JSON.
8. Flask displays the results in an interactive dashboard.

## 6. Project Structure

```text
ai-resume-matcher/
│
├── backend/
│   ├── requirements.txt
│   │
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── resume_parser.py
│       ├── resume_extractor.py
│       ├── jd_extractor.py
│       ├── matching_engine.py
│       ├── resume_validator.py
│       └── skill_gap_analyzer.py
│
├── frontend/
│   ├── app.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       └── style.css
│
└── README.md
```

## 7. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Ollama
- Git
- VS Code or another Python IDE

### Step 1: Clone the Repository

```bash
git clone "https://github.com/monish5599/ai-resume-matcher"
cd ai-resume-matcher
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r backend/requirements.txt
```

If Flask and Requests are not included in your backend requirements, install them separately:

```bash
pip install flask requests
```

### Step 4: Set Up Ollama

Download and install Ollama from:

https://ollama.com/

Download the required model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before starting the application.

## 8. Running the Application

The frontend and backend run separately.

### Start the FastAPI Backend

Open the first terminal:

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

FastAPI Swagger documentation:

http://127.0.0.1:8000/docs

### Start the Flask Frontend

Open a second terminal from the project root:

```powershell
python frontend/app.py
```

Frontend URL:

http://127.0.0.1:5000

Open the frontend URL in your browser to start analyzing resumes.

## 9. API Endpoints

| Method | Endpoint          | Description                              |
| ------ | ----------------- | ---------------------------------------- |
| GET    | `/`               | Checks API availability                  |
| POST   | `/resumes/upload` | Uploads and analyzes a resume            |
| POST   | `/jobs/match`     | Compares a resume with a job description |

### Resume Upload

Endpoint:

```http
POST /resumes/upload
```

Request: Multipart form data containing a PDF file.

### Job Matching

Endpoint:

```http
POST /jobs/match
```

Request: Multipart form data containing:

- `file`: Resume PDF
- `job_description`: Job description text

Response includes:

- Extracted resume information
- Extracted job requirements
- Matching results
- Skill gap recommendations

## 10. Matching Logic

The matching engine compares candidate skills against required skills from the job description.

The current matching approach considers:

- Exact skill matches.
- Alternative skill matches.
- Related skill matches.
- Missing required skills.
- Matched preferred skills.

The match percentage is calculated using required skills. Preferred skills are reported separately.

**Note:** The match percentage represents skill compatibility based on the extracted requirements. It is not a complete assessment of a candidate's overall suitability for a job.

## 11. Screenshots

Add screenshots of your application here.

Suggested screenshots:

- Resume upload interface.
- Job description input.
- Resume match percentage dashboard.
- Matched and missing skills.
- AI skill gap recommendations.
- Extracted resume information.

Example:

```markdown
![Resume Matcher Dashboard](screenshots/dashboard.png)
```

## 12. Limitations and Future Enhancements

### Current Limitations

- Currently supports PDF resume uploads.
- Scanned PDFs containing images may require OCR.
- Extraction accuracy depends on resume formatting and the language model.
- Match percentage is primarily based on required skill matching.
- AI-extracted information may require manual verification.

### Future Enhancements

- OCR support for scanned resumes.
- Improved semantic skill matching.
- Experience and education-based matching.
- Resume improvement recommendations.
- Downloadable analysis reports.
- User authentication and analysis history.
- Cloud deployment.

## 13. Author

**Monish V.**

BE Computer Science and Engineering – AI & ML

GitHub: https://github.com/monish5599

LinkedIn: https://www.linkedin.com/in/monish-v-656535251/

---

Built with Python, FastAPI, Flask, and Ollama
