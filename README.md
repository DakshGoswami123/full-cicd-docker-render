# Full CI/CD Pipeline with Docker and Live Cloud Deployment

## 1. Project Overview

This project is a complete beginner-friendly DevOps demonstration built for students. It shows how a simple Flask application can move from source code to automated testing, Docker packaging, security validation, and live cloud deployment.

The application is intentionally simple so the focus stays on the DevOps workflow.

The home page shows:

- `App Running`
- application version
- build reference
- deployment timestamp
- summary of the CI/CD process

## 2. Project Goal

The goal is to prove that a code push can automatically trigger a real CI/CD pipeline that:

1. validates the application with tests
2. audits Python dependencies for security issues
3. builds a Docker image
4. pushes the image to Docker Hub
5. deploys the app to Render
6. exposes the app on a public URL

## 3. Key Features

- Flask application with professional project dashboard UI
- Health endpoint for uptime checks
- Metadata endpoint for demo and monitoring
- Automated testing using `pytest`
- Dependency security audit using `pip-audit`
- Dockerfile for containerized deployment
- `docker-compose.yml` for local execution
- GitHub Actions CI/CD pipeline
- Docker Hub push with image tagging
- Render cloud deployment using deploy hook
- Beginner-friendly setup scripts for Windows and Linux

## 4. Folder Structure

```text
.
|-- .github/
|   `-- workflows/
|       `-- ci-cd.yml
|-- app/
|   |-- __init__.py
|   `-- main.py
|-- AutoTesting/
|   `-- test_app.py
|-- .dockerignore
|-- .env.example
|-- .gitignore
|-- Dockerfile
|-- docker-compose.yml
|-- FACULTY_DEMO_SCRIPT.md
|-- README.md
|-- render.yaml
|-- requirements.txt
|-- setup.bat
`-- setup.sh
```

## 5. Architecture Diagram

```text
Developer Pushes Code
        |
        v
   GitHub Repository
        |
        v
 GitHub Actions Workflow
   - Checkout code
   - Install dependencies
   - Run tests
   - Run dependency security audit
   - Build Docker image
   - Push image to Docker Hub
   - Trigger Render deploy hook
        |
        v
 Render Builds And Deploys App
        |
        v
   Public Live URL
```

## 6. Application Endpoints

- `/` -> Main UI page showing status and project details
- `/health` -> Returns `{"status":"healthy"}`
- `/api/info` -> Returns JSON metadata for version, build reference, and deployment information

## 7. Local Setup

### Option A: Windows

```bat
setup.bat
```

### Option B: Linux / macOS / Git Bash

```bash
chmod +x setup.sh
./setup.sh
```

### Option C: Manual

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

## 8. Run With Docker

### Build and run

```bash
docker build -t flask-devops-live .
docker run -p 5000:5000 -e APP_VERSION=1.0.0 flask-devops-live
```

### Run with Docker Compose

```bash
docker compose up --build
```

Open:

```text
http://localhost:5000
```

## 9. CI/CD Workflow Explanation

The workflow file is:

`.github/workflows/ci-cd.yml`

### Stage 1: Test

- GitHub Actions checks out the repository
- Python is installed
- dependencies are installed from `requirements.txt`
- tests from `AutoTesting/` are executed

### Stage 2: Dependency Security Audit

- `pip-audit` scans Python dependencies
- a JSON report is generated
- the report is uploaded as a GitHub Actions artifact

This is the extra DevOps feature added to make the project stronger academically and professionally.

### Stage 3: Docker Build and Push

- Docker image is built
- image is tagged as `latest`
- image is also tagged with the Git commit SHA
- image is pushed to Docker Hub

### Stage 4: Render Deployment

- GitHub Actions checks that the Render deploy hook secret exists
- the deploy hook is triggered
- Render pulls the latest GitHub source and redeploys the application

## 10. Important Clarification About Deployment

This project uses both Docker Hub and Render, but they serve slightly different purposes:

- Docker Hub stores the built image as part of the CI/CD pipeline
- Render deploy hook performs the live cloud deployment from the connected GitHub repository

This still counts as a real CI/CD pipeline because:

- tests and security checks happen automatically
- image build and push happen automatically
- deployment happens automatically after pipeline success

## 11. GitHub Secrets Required

In your GitHub repository, open:

`Settings -> Secrets and variables -> Actions`

Add:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `RENDER_DEPLOY_HOOK_URL`

## 12. Publish To GitHub

### Step 1: Create a new empty GitHub repository

Create a repository such as:

```text
full-cicd-docker-render
```

Do not add a README from GitHub because this project already contains one.

### Step 2: Push this local project

Run these commands inside the project folder:

```bash
git init
git add .
git commit -m "Initial commit: full CI/CD DevOps project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

### Step 3: Verify GitHub files

Once pushed, check that these files exist in GitHub:

- `.github/workflows/ci-cd.yml`
- `Dockerfile`
- `docker-compose.yml`
- `render.yaml`
- `README.md`

## 13. Deploy On Render

### Step 1: Create Docker Hub token

1. Sign in to Docker Hub
2. Open account settings
3. Create a personal access token
4. Copy the token
5. Add it to GitHub as `DOCKERHUB_TOKEN`

### Step 2: Create Render blueprint service

1. Sign in to Render
2. Click `New +`
3. Select `Blueprint`
4. Connect your GitHub account
5. Choose this repository
6. Render will detect `render.yaml`
7. Create the service

The current Render config in [render.yaml](./render.yaml) uses:

- `runtime: docker`
- `healthCheckPath: /health`
- `autoDeployTrigger: off`

`autoDeployTrigger: off` is important because GitHub Actions controls when deployment happens.

### Step 3: Set Render environment variables

In the Render dashboard, set:

- `APP_VERSION=1.0.0`

Optional values you can later change for demonstration:

- `APP_VERSION=1.0.1`
- `APP_VERSION=2.0.0`

### Step 4: Create Render deploy hook

1. Open the created Render service
2. Go to `Settings`
3. Copy the `Deploy Hook` URL
4. Add it to GitHub Secrets as `RENDER_DEPLOY_HOOK_URL`

### Step 5: Trigger deployment

Push any code change to `main`.

GitHub Actions will:

1. run tests
2. run dependency audit
3. build Docker image
4. push Docker image to Docker Hub
5. call the Render deploy hook

Render will then build and deploy the latest code.

### Step 6: Open the live URL

Render will provide a public address similar to:

```text
https://flask-devops-live.onrender.com
```

## 14. What To Demonstrate Live

### Screen 1: Application UI

Open:

```text
http://localhost:5000
```

Show:

- application is running
- version is visible
- project title is visible
- build and deploy details are visible

### Screen 2: Tests

Open [AutoTesting/test_app.py](./AutoTesting/test_app.py)

Explain:

- root page is tested
- health endpoint is tested
- metadata endpoint is tested

### Screen 3: Workflow

Open [.github/workflows/ci-cd.yml](./.github/workflows/ci-cd.yml)

Explain the four stages:

- test
- security audit
- docker build and push
- deploy to Render

### Screen 4: Docker

Open [Dockerfile](./Dockerfile) and [docker-compose.yml](./docker-compose.yml)

Explain:

- same app can run on any system using the container
- this avoids “works on my machine” issues

### Screen 5: Cloud Deployment

Open [render.yaml](./render.yaml)

Explain:

- health check path
- Docker runtime
- deployment trigger handled by GitHub Actions

### Screen 6: Public URL

Open the Render public URL after deployment completes.

## 15. Demo Update Strategy

To show automatic update after push:

1. change `APP_VERSION` in Render or update application text
2. commit and push the code
3. open GitHub Actions and show the workflow running
4. wait for success
5. refresh the Render public URL
6. show that the new version appears

## 16. Resume Description

Built a complete DevOps automation project using Flask, Docker, GitHub Actions, Docker Hub, and Render. Implemented automated testing, dependency security auditing, container image publishing, and live cloud deployment triggered after successful pipeline execution.

## 17. Faculty-Facing Explanation

This project demonstrates how DevOps reduces manual work in software delivery. Instead of testing, packaging, and deploying by hand, the entire flow is automated. When a developer pushes code, GitHub Actions validates the code, checks dependency security, creates a Docker image, pushes it to Docker Hub, and triggers deployment on Render. The final result is a live application available on a public URL.

## 18. Viva Questions

1. What is the difference between CI and CD?
2. Why is Docker used in this project?
3. Why do we store secrets in GitHub Secrets?
4. What is the purpose of the `/health` endpoint?
5. What does `pip-audit` do?
6. Why are automated tests important before deployment?
7. What is a deploy hook in Render?
8. What is the role of Docker Hub in this project?
9. What happens when a push is made to the `main` branch?
10. Why is the application logic simple in this project?

## 19. Important Notes

- The project is fully runnable locally.
- The pipeline is real and ready to work once your secrets are configured.
- The project is intentionally simple in logic but strong in DevOps coverage.
- This is suitable for mini-project demonstrations, internships, portfolio discussion, and faculty viva.
