# AI Resume Analyzer with Automated CI/CD Pipeline

## Overview

This project is a simple Flask-based AI Resume Analyzer designed for fast college demos and viva presentations.

A user can:

- upload a resume in PDF or TXT format
- analyze resume text instantly
- view word count, detected skills, resume score, and improvement suggestions

The same project is connected to a full DevOps workflow using:

- GitHub Actions
- Docker
- Docker Hub
- Render
- pytest
- pip-audit

## What The Project Does

The application performs lightweight resume analysis without heavy machine learning models.

It:

- extracts text from PDF or TXT resumes
- counts words
- detects common technical skills
- calculates a simple score
- gives 2 to 3 improvement suggestions

This keeps the project reliable, fast, and easy to explain in under 2 minutes.

## Main Endpoints

- `/` -> Resume Analyzer UI
- `/upload` -> Upload and analyze PDF or TXT resume
- `/analyze` -> Analyze pasted resume text
- `/health` -> Health check
- `/api/info` -> App metadata

For raw JSON, use:

- `/health?raw=1`
- `/api/info?raw=1`
- `/upload?raw=1`

## CI/CD Flow

Whenever code is pushed to GitHub:

1. GitHub Actions checks out the code
2. pytest runs automated tests
3. pip-audit checks dependency security
4. Docker image is built
5. image is pushed to Docker Hub
6. Render deploy hook is triggered
7. live application updates automatically

## Local Run

### Option 1: Windows

```bat
setup.bat
```

### Option 2: Linux / macOS / Git Bash

```bash
chmod +x setup.sh
./setup.sh
```

### Option 3: Manual

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest AutoTesting -q
python -m flask --app app.main run --host=0.0.0.0 --port=5000
```

Then open:

```text
http://localhost:5000
```

## Docker Run

```bash
docker build -t ai-resume-analyzer .
docker run -p 5000:5000 -e APP_VERSION=1.0.0 ai-resume-analyzer
```

Or:

```bash
docker compose up --build
```

## Demo Flow

For a 2-minute demo, show:

1. Home page
2. Upload a TXT or PDF resume
3. Show detected skills, score, and suggestions
4. Open GitHub Actions workflow
5. Show Render live URL

## Why This Project Is Good For Viva

- Simple to explain
- Uses AI-style analysis without heavy infrastructure
- Demonstrates Flask development and DevOps automation together
- Works quickly and reliably in live demos

## Tech Stack

- Flask
- PyPDF2
- pytest
- pip-audit
- Docker
- GitHub Actions
- Docker Hub
- Render

## Confirmation

This project is designed to be:

- demo-ready
- CI/CD-ready
- Docker-ready
- Render-ready
- beginner-friendly
