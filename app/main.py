import os
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string, request


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    def wants_raw_json() -> bool:
        """Return JSON for tests, scripts, and explicit raw requests."""
        return request.args.get("raw") == "1" or request.accept_mimetypes.best == "application/json"

    def render_status_page(title: str, payload: dict) -> str:
        """Render a small browser-friendly status page for demo endpoints."""
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

    @app.get("/")
    def home():
        version = os.getenv("APP_VERSION", "1.0.0")
        project_title = "Full CI/CD Pipeline with Docker and Live Cloud Deployment"
        build_ref = (os.getenv("BUILD_REF") or os.getenv("RENDER_GIT_COMMIT") or "local-demo")[:12]
        deployed_at = os.getenv("DEPLOYED_AT") or (
            "render-runtime" if os.getenv("RENDER") == "true"
            else datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        )
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ project_title }}</title>
            <style>
                :root {
                    --bg: #eef3f8;
                    --bg-accent: #dfe8f2;
                    --navy: #11324d;
                    --slate: #4a647e;
                    --card: rgba(255, 255, 255, 0.92);
                    --line: rgba(17, 50, 77, 0.12);
                    --text-main: #182635;
                    --text-muted: #5c7289;
                    --success: #1d7f5f;
                    --teal: #1f6f8b;
                    --gold: #b8860b;
                }
                body {
                    font-family: Georgia, "Times New Roman", serif;
                    background:
                        radial-gradient(circle at top left, rgba(31, 111, 139, 0.14), transparent 24%),
                        linear-gradient(180deg, var(--bg), var(--bg-accent));
                    margin: 0;
                    color: var(--text-main);
                }
                .page {
                    max-width: 1180px;
                    margin: 0 auto;
                    padding: 28px 20px 48px;
                }
                .topbar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    gap: 12px;
                    margin-bottom: 18px;
                    padding: 14px 18px;
                    border-radius: 18px;
                    background: rgba(255, 255, 255, 0.75);
                    border: 1px solid var(--line);
                }
                .topbar-title {
                    font-size: 0.95rem;
                    color: var(--navy);
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    font-weight: 700;
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                .topbar-meta {
                    color: var(--text-muted);
                    font-size: 0.95rem;
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                .hero {
                    display: grid;
                    grid-template-columns: 1.4fr 1fr;
                    gap: 24px;
                    align-items: stretch;
                    margin-bottom: 24px;
                }
                .panel {
                    background: var(--card);
                    border: 1px solid var(--line);
                    border-radius: 24px;
                    box-shadow: 0 18px 40px rgba(17, 50, 77, 0.08);
                }
                .hero-copy {
                    padding: 34px;
                }
                .eyebrow {
                    display: inline-block;
                    padding: 8px 14px;
                    border-radius: 999px;
                    background: rgba(17, 50, 77, 0.08);
                    color: var(--navy);
                    font-weight: bold;
                    letter-spacing: 0.05em;
                    text-transform: uppercase;
                    font-size: 0.78rem;
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                h1 {
                    font-size: clamp(2.2rem, 4vw, 4rem);
                    line-height: 1.05;
                    margin: 18px 0 14px;
                    color: var(--navy);
                }
                .lead {
                    color: var(--text-muted);
                    font-size: 1.08rem;
                    line-height: 1.7;
                    max-width: 58ch;
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                .status-grid {
                    display: grid;
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                    gap: 14px;
                    margin-top: 28px;
                }
                .stat {
                    padding: 18px;
                    border-radius: 18px;
                    background: rgba(255, 255, 255, 0.85);
                    border: 1px solid var(--line);
                }
                .stat-label {
                    color: var(--text-muted);
                    font-size: 0.82rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin-bottom: 10px;
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                .stat-value {
                    font-size: 1.15rem;
                    font-weight: 700;
                    color: var(--navy);
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                .hero-side {
                    padding: 24px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                }
                .health {
                    padding: 16px 18px;
                    border-radius: 18px;
                    background: rgba(29, 127, 95, 0.08);
                    border: 1px solid rgba(29, 127, 95, 0.18);
                    color: var(--text-main);
                    margin-bottom: 18px;
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                .health strong {
                    color: var(--success);
                }
                .pipeline-title {
                    margin: 0 0 16px;
                    font-size: 1.1rem;
                    color: var(--navy);
                }
                .pipeline-step {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 12px 0;
                    color: var(--text-muted);
                    border-top: 1px solid var(--line);
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                .pipeline-step:first-of-type {
                    border-top: none;
                }
                .step-dot {
                    width: 34px;
                    height: 34px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: rgba(17, 50, 77, 0.1);
                    color: var(--teal);
                    font-weight: 700;
                    flex-shrink: 0;
                }
                .section-grid {
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 18px;
                }
                .info-card {
                    padding: 24px;
                }
                .info-card h2 {
                    margin-top: 0;
                    margin-bottom: 12px;
                    font-size: 1.2rem;
                    color: var(--navy);
                }
                .info-card p, .info-card li {
                    color: var(--text-muted);
                    line-height: 1.65;
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                .info-card li + li {
                    margin-top: 8px;
                }
                ul {
                    padding-left: 18px;
                    margin: 0;
                }
                .demo-banner {
                    margin-top: 22px;
                    padding: 18px 20px;
                    border-radius: 18px;
                    background: rgba(184, 134, 11, 0.08);
                    border: 1px solid rgba(184, 134, 11, 0.2);
                    color: var(--text-main);
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                .demo-banner strong {
                    color: var(--gold);
                }
                .footer-note {
                    margin-top: 16px;
                    color: var(--text-muted);
                    font-size: 0.95rem;
                    font-family: "Segoe UI", Arial, sans-serif;
                }
                @media (max-width: 900px) {
                    .hero, .section-grid {
                        grid-template-columns: 1fr;
                    }
                    .page {
                        padding: 18px 14px 32px;
                    }
                    .hero-copy, .hero-side, .info-card {
                        padding: 20px;
                    }
                    .status-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="page">
                <div class="topbar">
                    <div class="topbar-title">Department Project Demonstration</div>
                    <div class="topbar-meta">Build Reference: {{ build_ref }} | Deployed At: {{ deployed_at }}</div>
                </div>

                <section class="hero">
                    <div class="panel hero-copy">
                        <span class="eyebrow">{{ project_title }}</span>
                        <h1>App Running</h1>
                        <p class="lead">
                            This project demonstrates a complete DevOps workflow using Flask, Docker,
                            GitHub Actions, Docker Hub, and Render. Every push can run tests, build a
                            container image, and trigger a live cloud deployment.
                        </p>

                        <div class="status-grid">
                            <div class="stat">
                                <div class="stat-label">Version</div>
                                <div class="stat-value">{{ version }}</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">Application Status</div>
                                <div class="stat-value">Healthy and Reachable</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">Tech Stack</div>
                                <div class="stat-value">Flask + Docker + GitHub Actions</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">Deployment Target</div>
                                <div class="stat-value">Render Public Web Service</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">Security Gate</div>
                                <div class="stat-value">Dependency Audit Before Release</div>
                            </div>
                            <div class="stat">
                                <div class="stat-label">Build Reference</div>
                                <div class="stat-value">{{ build_ref }}</div>
                            </div>
                        </div>
                    </div>

                    <div class="panel hero-side">
                        <div class="health">
                            <strong>Live Status:</strong> The application container is up and serving requests.
                        </div>
                        <div>
                            <h2 class="pipeline-title">Pipeline Flow</h2>
                            <div class="pipeline-step"><span class="step-dot">1</span> Push code to GitHub</div>
                            <div class="pipeline-step"><span class="step-dot">2</span> Run automated tests from AutoTesting</div>
                            <div class="pipeline-step"><span class="step-dot">3</span> Build Docker image</div>
                            <div class="pipeline-step"><span class="step-dot">4</span> Push image to Docker Hub</div>
                            <div class="pipeline-step"><span class="step-dot">5</span> Trigger Render deployment</div>
                            <div class="pipeline-step"><span class="step-dot">6</span> Access updated app on public URL</div>
                        </div>
                    </div>
                </section>

                <section class="section-grid">
                    <article class="panel info-card">
                        <h2>Project Purpose</h2>
                        <p>
                            The goal of this project is to show a real end-to-end CI/CD pipeline
                            rather than complex business logic. It is designed for student demos,
                            viva sessions, portfolio projects, and beginner DevOps practice with
                            a strong focus on automation and deployment confidence.
                        </p>
                    </article>

                    <article class="panel info-card">
                        <h2>Academic Talking Points</h2>
                        <ul>
                            <li>Continuous Integration validates every code push with automated tests.</li>
                            <li>Containerization ensures the same build runs locally and in the cloud.</li>
                            <li>Continuous Deployment reduces manual release steps and human error.</li>
                            <li>Security auditing blocks unsafe dependency changes before release.</li>
                            <li>Health checks help the platform verify service availability.</li>
                        </ul>
                    </article>

                    <article class="panel info-card">
                        <h2>Submission Summary</h2>
                        <p>
                            This is a complete student-friendly DevOps project that combines source
                            control, automated testing, security checks, Docker image creation,
                            cloud deployment, and public accessibility in one workflow.
                        </p>
                    </article>
                </section>

                <div class="demo-banner">
                    <strong>Live Demo Tip:</strong> Change the version number, push the code, show the GitHub Actions run,
                    and refresh the deployed URL to demonstrate automatic updates after deployment.
                </div>

                <div class="footer-note">
                    Suggested faculty demo order: homepage, tests, workflow, Dockerfile, Render config, and then the live cloud URL.
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(
            html,
            version=version,
            project_title=project_title,
            build_ref=build_ref,
            deployed_at=deployed_at,
        )

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
            "project": "Full CI/CD Pipeline with Docker and Live Cloud Deployment",
            "status": "running",
            "version": os.getenv("APP_VERSION", "1.0.0"),
            "build_ref": (os.getenv("BUILD_REF") or os.getenv("RENDER_GIT_COMMIT") or "local-demo")[
                :12
            ],
            "deployed_at": os.getenv("DEPLOYED_AT")
            or ("render-runtime" if os.getenv("RENDER") == "true" else "not-set"),
        }
        if wants_raw_json():
            return jsonify(payload), 200
        return render_status_page("Application Metadata", payload), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
