import io
import os
from datetime import datetime, timezone

from PyPDF2 import PdfReader
from flask import Flask, jsonify, render_template_string, request


SKILL_KEYWORDS = [
    "python",
    "java",
    "sql",
    "flask",
    "django",
    "docker",
    "git",
    "github actions",
    "aws",
    "azure",
    "gcp",
    "kubernetes",
    "linux",
    "html",
    "css",
    "javascript",
    "react",
    "machine learning",
    "data analysis",
]

ALLOWED_EXTENSIONS = {".pdf", ".txt"}


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    def wants_raw_json() -> bool:
        """Return JSON for tests, scripts, and explicit raw requests."""
        return request.args.get("raw") == "1" or request.accept_mimetypes.best == "application/json"

    def deployment_metadata() -> dict:
        """Return deployment information shown in the UI and info endpoint."""
        return {
            "project": "AI Resume Analyzer with Automated CI/CD Pipeline",
            "version": os.getenv("APP_VERSION", "1.0.0"),
            "build_ref": (os.getenv("BUILD_REF") or os.getenv("RENDER_GIT_COMMIT") or "local-demo")[:12],
            "deployed_at": os.getenv("DEPLOYED_AT")
            or ("render-runtime" if os.getenv("RENDER") == "true" else datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")),
        }

    def render_status_page(title: str, payload: dict) -> str:
        """Render a browser-friendly status page for demo endpoints."""
        pretty_payload = "{\n" + ",\n".join(
            f'  "{key}": "{value}"' for key, value in payload.items()
        ) + "\n}"
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                body {
                    margin: 0;
                    font-family: "Segoe UI", Arial, sans-serif;
                    background: linear-gradient(180deg, #eef4f9, #dce8f4);
                    color: #17324a;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 24px;
                }
                .card {
                    width: min(760px, 100%);
                    background: white;
                    border-radius: 22px;
                    padding: 28px;
                    box-shadow: 0 18px 45px rgba(17, 50, 77, 0.12);
                    border: 1px solid rgba(17, 50, 77, 0.12);
                }
                h1 {
                    margin: 0 0 8px;
                    color: #11324d;
                }
                p {
                    color: #587188;
                    line-height: 1.6;
                }
                pre {
                    margin-top: 18px;
                    padding: 18px;
                    border-radius: 16px;
                    background: #0f2235;
                    color: #dff4ff;
                    overflow-x: auto;
                    font-size: 0.98rem;
                }
                .hint {
                    margin-top: 14px;
                    font-size: 0.95rem;
                    color: #587188;
                }
                code {
                    background: #edf4fb;
                    padding: 2px 6px;
                    border-radius: 6px;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>{{ title }}</h1>
                <p>This endpoint is working correctly. For browser demos it is shown in a readable format.</p>
                <pre>{{ pretty_payload }}</pre>
                <div class="hint">Use <code>?raw=1</code> if you want machine-readable JSON.</div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html, title=title, pretty_payload=pretty_payload)

    def extract_resume_text(uploaded_file) -> tuple[str, str]:
        """Extract text from a PDF or plain text resume uploaded through the form."""
        if uploaded_file is None or uploaded_file.filename == "":
            raise ValueError("Please upload a resume file.")

        extension = os.path.splitext(uploaded_file.filename)[1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise ValueError("Only PDF and TXT resumes are supported for this demo.")

        file_bytes = uploaded_file.read()
        if not file_bytes:
            raise ValueError("The uploaded resume is empty.")

        if extension == ".pdf":
            reader = PdfReader(io.BytesIO(file_bytes))
            extracted = " ".join((page.extract_text() or "") for page in reader.pages).strip()
        else:
            extracted = file_bytes.decode("utf-8", errors="ignore").strip()

        if not extracted:
            raise ValueError("No readable text was found in the uploaded resume.")

        return extracted, uploaded_file.filename

    def analyze_resume_text(text: str, source_name: str = "Typed Resume Text") -> dict:
        """Perform a fast keyword-based resume analysis suitable for live demos."""
        normalized = " ".join(text.split())
        lowered = normalized.lower()
        word_count = len(normalized.split())
        matched_skills = [skill.title() for skill in SKILL_KEYWORDS if skill in lowered]

        score = 35
        if word_count >= 120:
            score += 20
        elif word_count >= 60:
            score += 12

        score += min(len(matched_skills) * 8, 40)
        if any(keyword in lowered for keyword in ["project", "experience", "internship", "certification"]):
            score += 5
        score = min(score, 100)

        suggestions = []
        if word_count < 80:
            suggestions.append("Add more detail about projects, internships, and measurable impact.")
        if len(matched_skills) < 4:
            suggestions.append("Include more role-relevant technical skills and tools in the resume.")
        if "github" not in lowered and "portfolio" not in lowered:
            suggestions.append("Add a GitHub or portfolio link to make your profile stronger.")
        if not suggestions:
            suggestions = [
                "Tailor the summary and skills section for the exact job role.",
                "Keep achievement bullets result-focused with numbers where possible.",
                "Review formatting for consistent headings and concise bullet points.",
            ]

        preview = normalized[:350] + ("..." if len(normalized) > 350 else "")
        return {
            "source_name": source_name,
            "word_count": word_count,
            "skills_found": matched_skills,
            "score": score,
            "suggestions": suggestions[:3],
            "preview": preview,
        }

    def render_home(result: dict | None = None, error_message: str | None = None, resume_text: str = "") -> str:
        """Render the main AI Resume Analyzer UI."""
        metadata = deployment_metadata()
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ metadata.project }}</title>
            <style>
                :root {
                    --bg: #edf4fb;
                    --bg-accent: #dce8f3;
                    --navy: #14324b;
                    --teal: #1f6f8b;
                    --green: #1d7f5f;
                    --gold: #ae7c14;
                    --card: rgba(255, 255, 255, 0.94);
                    --line: rgba(20, 50, 75, 0.12);
                    --text: #162737;
                    --muted: #5b7287;
                    --danger-bg: #fff1ef;
                    --danger-text: #9e3d31;
                }
                body {
                    margin: 0;
                    font-family: "Segoe UI", Arial, sans-serif;
                    color: var(--text);
                    background:
                        radial-gradient(circle at top left, rgba(31, 111, 139, 0.14), transparent 25%),
                        linear-gradient(180deg, var(--bg), var(--bg-accent));
                }
                .page {
                    max-width: 1180px;
                    margin: 0 auto;
                    padding: 28px 18px 40px;
                }
                .topbar {
                    display: flex;
                    justify-content: space-between;
                    gap: 12px;
                    padding: 14px 18px;
                    border-radius: 18px;
                    background: rgba(255, 255, 255, 0.78);
                    border: 1px solid var(--line);
                    margin-bottom: 18px;
                    font-size: 0.95rem;
                }
                .topbar strong {
                    color: var(--navy);
                    text-transform: uppercase;
                    letter-spacing: 0.06em;
                    font-size: 0.84rem;
                }
                .hero {
                    display: grid;
                    grid-template-columns: 1.15fr 0.85fr;
                    gap: 22px;
                    margin-bottom: 22px;
                }
                .panel {
                    background: var(--card);
                    border-radius: 24px;
                    border: 1px solid var(--line);
                    box-shadow: 0 18px 40px rgba(20, 50, 75, 0.08);
                }
                .hero-copy {
                    padding: 30px;
                }
                .eyebrow {
                    display: inline-block;
                    padding: 8px 14px;
                    border-radius: 999px;
                    background: rgba(20, 50, 75, 0.08);
                    color: var(--navy);
                    font-size: 0.78rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    font-weight: 700;
                }
                h1 {
                    font-family: Georgia, "Times New Roman", serif;
                    color: var(--navy);
                    margin: 18px 0 12px;
                    font-size: clamp(2.1rem, 4vw, 3.5rem);
                    line-height: 1.05;
                }
                .lead {
                    color: var(--muted);
                    line-height: 1.75;
                    max-width: 62ch;
                    margin-bottom: 20px;
                }
                .stats {
                    display: grid;
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                    gap: 14px;
                }
                .stat {
                    background: rgba(255, 255, 255, 0.9);
                    border: 1px solid var(--line);
                    border-radius: 18px;
                    padding: 16px;
                }
                .stat-label {
                    color: var(--muted);
                    font-size: 0.8rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin-bottom: 10px;
                }
                .stat-value {
                    color: var(--navy);
                    font-weight: 700;
                    font-size: 1.05rem;
                }
                .hero-side {
                    padding: 24px;
                }
                .flow-title {
                    margin: 0 0 12px;
                    color: var(--navy);
                    font-size: 1.15rem;
                }
                .flow-step {
                    display: flex;
                    gap: 12px;
                    align-items: center;
                    padding: 12px 0;
                    border-top: 1px solid var(--line);
                    color: var(--muted);
                }
                .flow-step:first-of-type {
                    border-top: none;
                }
                .step-dot {
                    width: 34px;
                    height: 34px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: rgba(31, 111, 139, 0.12);
                    color: var(--teal);
                    font-weight: 700;
                    flex-shrink: 0;
                }
                .workspace {
                    display: grid;
                    grid-template-columns: 0.95fr 1.05fr;
                    gap: 22px;
                }
                .form-panel, .result-panel {
                    padding: 26px;
                }
                h2 {
                    color: var(--navy);
                    margin-top: 0;
                }
                label {
                    display: block;
                    font-weight: 600;
                    margin: 16px 0 8px;
                    color: var(--navy);
                }
                input[type="file"], textarea {
                    width: 100%;
                    box-sizing: border-box;
                    border: 1px solid var(--line);
                    border-radius: 16px;
                    padding: 14px;
                    font: inherit;
                    background: #fbfdff;
                }
                textarea {
                    min-height: 180px;
                    resize: vertical;
                }
                .button-row {
                    display: flex;
                    gap: 12px;
                    flex-wrap: wrap;
                    margin-top: 18px;
                }
                button {
                    border: none;
                    border-radius: 999px;
                    padding: 12px 18px;
                    font: inherit;
                    font-weight: 700;
                    cursor: pointer;
                }
                .primary {
                    background: var(--navy);
                    color: white;
                }
                .secondary {
                    background: rgba(31, 111, 139, 0.12);
                    color: var(--teal);
                }
                .error {
                    margin-top: 16px;
                    padding: 14px 16px;
                    border-radius: 14px;
                    background: var(--danger-bg);
                    color: var(--danger-text);
                    border: 1px solid rgba(158, 61, 49, 0.18);
                }
                .result-empty {
                    color: var(--muted);
                    line-height: 1.7;
                }
                .score-card {
                    display: inline-flex;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 14px;
                    padding: 12px 16px;
                    border-radius: 16px;
                    background: rgba(29, 127, 95, 0.1);
                    border: 1px solid rgba(29, 127, 95, 0.18);
                    color: var(--green);
                    font-weight: 700;
                }
                .result-grid {
                    display: grid;
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                    gap: 12px;
                    margin-bottom: 16px;
                }
                .result-box {
                    border: 1px solid var(--line);
                    border-radius: 16px;
                    padding: 14px;
                    background: rgba(255, 255, 255, 0.84);
                }
                .result-box strong {
                    display: block;
                    color: var(--navy);
                    margin-bottom: 8px;
                }
                .skills {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                }
                .skill {
                    padding: 8px 10px;
                    border-radius: 999px;
                    background: rgba(31, 111, 139, 0.1);
                    color: var(--teal);
                    font-size: 0.92rem;
                    font-weight: 600;
                }
                .suggestions {
                    margin: 0;
                    padding-left: 20px;
                    color: var(--muted);
                    line-height: 1.65;
                }
                .preview {
                    margin-top: 16px;
                    padding: 14px;
                    border-radius: 16px;
                    background: #0f2235;
                    color: #e4f5ff;
                    white-space: pre-wrap;
                    line-height: 1.55;
                }
                @media (max-width: 960px) {
                    .hero, .workspace {
                        grid-template-columns: 1fr;
                    }
                    .stats, .result-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="page">
                <div class="topbar">
                    <div><strong>AI Resume Analyzer with Automated CI/CD Pipeline</strong></div>
                    <div>Version: {{ metadata.version }} | Build: {{ metadata.build_ref }} | Deployed: {{ metadata.deployed_at }}</div>
                </div>

                <section class="hero">
                    <div class="panel hero-copy">
                        <span class="eyebrow">Fast 2-Minute Viva Demo</span>
                        <h1>Upload a Resume and Get Instant Analysis</h1>
                        <p class="lead">
                            This project combines a lightweight AI-style resume analyzer with a complete DevOps pipeline.
                            Users upload a PDF or text resume, receive instant keyword-based analysis, and every GitHub
                            push still goes through testing, security audit, Docker build, Docker Hub push, and live Render deployment.
                        </p>
                        <div class="stats">
                            <div class="stat">
                                <div class="stat-label">Upload Support</div>
                                <div class="stat-value">PDF and TXT resumes</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">Analysis Speed</div>
                                <div class="stat-value">1 to 2 seconds</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">Scoring Method</div>
                                <div class="stat-value">Word count + skills + sections</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">Deployment</div>
                                <div class="stat-value">Docker + GitHub Actions + Render</div>
                            </div>
                        </div>
                    </div>

                    <div class="panel hero-side">
                        <h2 class="flow-title">CI/CD Flow</h2>
                        <div class="flow-step"><span class="step-dot">1</span> Push code to GitHub</div>
                        <div class="flow-step"><span class="step-dot">2</span> Run pytest checks</div>
                        <div class="flow-step"><span class="step-dot">3</span> Run pip-audit security scan</div>
                        <div class="flow-step"><span class="step-dot">4</span> Build Docker image</div>
                        <div class="flow-step"><span class="step-dot">5</span> Push image to Docker Hub</div>
                        <div class="flow-step"><span class="step-dot">6</span> Trigger Render deployment</div>
                    </div>
                </section>

                <section class="workspace">
                    <div class="panel form-panel">
                        <h2>Resume Input</h2>
                        <form action="/upload" method="post" enctype="multipart/form-data">
                            <label for="resume_file">Upload PDF or TXT resume</label>
                            <input id="resume_file" name="resume_file" type="file" accept=".pdf,.txt">
                            <div class="button-row">
                                <button class="primary" type="submit">Upload and Analyze</button>
                            </div>
                        </form>

                        <form action="/analyze" method="post">
                            <label for="resume_text">Or paste resume text directly</label>
                            <textarea id="resume_text" name="resume_text" placeholder="Paste resume content here...">{{ resume_text }}</textarea>
                            <div class="button-row">
                                <button class="secondary" type="submit">Analyze Text</button>
                            </div>
                        </form>

                        {% if error_message %}
                        <div class="error">{{ error_message }}</div>
                        {% endif %}
                    </div>

                    <div class="panel result-panel">
                        <h2>Analysis Result</h2>
                        {% if result %}
                            <div class="score-card">Resume Score: {{ result.score }}/100</div>
                            <div class="result-grid">
                                <div class="result-box">
                                    <strong>Resume Source</strong>
                                    <span>{{ result.source_name }}</span>
                                </div>
                                <div class="result-box">
                                    <strong>Word Count</strong>
                                    <span>{{ result.word_count }} words</span>
                                </div>
                            </div>
                            <div class="result-box">
                                <strong>Skills Detected</strong>
                                <div class="skills">
                                    {% for skill in result.skills_found %}
                                        <span class="skill">{{ skill }}</span>
                                    {% endfor %}
                                    {% if not result.skills_found %}
                                        <span class="skill">No major keywords detected</span>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="result-box" style="margin-top: 14px;">
                                <strong>Suggestions</strong>
                                <ol class="suggestions">
                                    {% for suggestion in result.suggestions %}
                                        <li>{{ suggestion }}</li>
                                    {% endfor %}
                                </ol>
                            </div>
                            <div class="preview">{{ result.preview }}</div>
                        {% else %}
                            <p class="result-empty">
                                Upload a resume or paste text to see the analysis here. This keeps the demo simple:
                                one upload, instant result, and clear talking points for viva.
                            </p>
                        {% endif %}
                    </div>
                </section>
            </div>
        </body>
        </html>
        """
        return render_template_string(
            html,
            metadata=metadata,
            result=result,
            error_message=error_message,
            resume_text=resume_text,
        )

    @app.get("/")
    def home():
        return render_home()

    @app.post("/upload")
    def upload():
        """Accept a resume file, extract text, and return analysis."""
        try:
            extracted_text, filename = extract_resume_text(request.files.get("resume_file"))
            result = analyze_resume_text(extracted_text, source_name=filename)
        except ValueError as exc:
            if wants_raw_json():
                return jsonify({"error": str(exc)}), 400
            return render_home(error_message=str(exc)), 400

        if wants_raw_json():
            return jsonify(result), 200
        return render_home(result=result)

    @app.post("/analyze")
    def analyze():
        """Analyze resume text provided directly through the UI or API."""
        resume_text = (request.form.get("resume_text") or "").strip()
        if not resume_text and request.is_json:
            resume_text = (request.get_json(silent=True) or {}).get("resume_text", "").strip()

        if not resume_text:
            error_message = "Please paste resume text before starting analysis."
            if wants_raw_json():
                return jsonify({"error": error_message}), 400
            return render_home(error_message=error_message), 400

        result = analyze_resume_text(resume_text)
        if wants_raw_json():
            return jsonify(result), 200
        return render_home(result=result, resume_text=resume_text)

    @app.get("/health")
    def health():
        """Health-check endpoint used by tests and Render."""
        payload = {"status": "healthy"}
        if wants_raw_json():
            return jsonify(payload), 200
        return render_status_page("Health Endpoint", payload), 200

    @app.get("/api/info")
    def info():
        """Project metadata endpoint useful for demos and operational checks."""
        payload = {
            **deployment_metadata(),
            "status": "running",
        }
        if wants_raw_json():
            return jsonify(payload), 200
        return render_status_page("Application Metadata", payload), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
