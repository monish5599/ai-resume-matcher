
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Maximum upload size: 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # Get uploaded resume
        resume = request.files.get("resume")

        # Get job description
        job_description = request.form.get(
            "job_description", ""
        ).strip()

        # Validate resume
        if not resume or not resume.filename:
            return render_template(
                "index.html",
                error="Please upload your resume."
            )

        # Validate PDF
        if not resume.filename.lower().endswith(".pdf"):
            return render_template(
                "index.html",
                error="Only PDF files are supported."
            )

        # Validate job description
        if not job_description:
            return render_template(
                "index.html",
                error="Please enter a job description."
            )

        try:

            # Read uploaded PDF
            resume_bytes = resume.read()

            # Send PDF and job description to FastAPI
            files = {
                "file": (
                    resume.filename,
                    resume_bytes,
                    "application/pdf"
                )
            }

            data = {
                "job_description": job_description
            }

            response = requests.post(
                f"{FASTAPI_URL}/jobs/match",
                files=files,
                data=data,
                timeout=300
            )

            # Check API response
            if response.status_code != 200:

                try:
                    error_data = response.json()
                    error_message = error_data.get(
                        "detail", "Resume analysis failed."
                    )
                except ValueError:
                    error_message = "Backend returned an error."

                return render_template(
                    "index.html",
                    error=str(error_message)
                )

            # Convert JSON response into Python dictionary
            result = response.json()

            # Display results
            return render_template(
                "index.html",
                result=result
            )

        except requests.exceptions.ConnectionError:

            return render_template(
                "index.html",
                error="Cannot connect to FastAPI. Please start the backend."
            )

        except requests.exceptions.Timeout:

            return render_template(
                "index.html",
                error="Analysis took too long. Please try again."
            )

        except requests.exceptions.RequestException as error:

            return render_template(
                "index.html",
                error=f"Request failed: {error}"
            )

    return render_template("index.html")


@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        error="File is too large. Maximum size is 10 MB."
    ), 413


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )
