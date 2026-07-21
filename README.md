# Dockerized Flask App → GitHub Container Registry (GHCR)

A Flask application containerized with Docker and automatically built and published to GitHub Container Registry using a dual-trigger GitHub Actions CI/CD pipeline.

## What This Project Demonstrates

- Writing a production-style cache-optimized Dockerfile
- Automating container builds and registry publishing with GitHub Actions
- Authenticating to GHCR using the auto-scoped secrets.GITHUB_TOKEN (no manual PAT required)
- Tagging strategy: semantic version tags on formal releases, commit-SHA tags on every push
- Debugging real CI/CD failures (workflow file placement, tag naming conventions)

## Architecture

```text
git push to main  ──────┐
                         ├──▶  GitHub Actions  ──▶  Docker Build  ──▶  Push to GHCR
GitHub Release published┘
```

The pipeline is triggered two ways:

| Trigger | When it fires | Image tags produced |
|---|---|---|
| push to main | Every commit pushed to main | latest, short commit SHA (e.g. a6b9b16) |
| release: published | A formal GitHub Release is published | latest, semantic version (e.g. 1.0.1) |

This mirrors how real teams separate **continuous integration** (every commit gets a traceable, pullable image) from **continuous delivery** (deliberate, versioned releases).

## Tech Stack

- **App:** Python 3.12, Flask
- **Container:** Docker (python:3.12-slim base image)
- **CI/CD:** GitHub Actions
- **Registry:** GitHub Container Registry (ghcr.io)
- **Actions used:** actions/checkout, docker/login-action, docker/metadata-action, docker/setup-buildx-action, docker/build-push-action

## Run It Yourself

Pull the published image directly — no build required:

```bash
docker pull ghcr.io/haseebspaniard/docker-ghcr-demo:latest
docker run -d -p 5000:5000 ghcr.io/haseebspaniard/docker-ghcr-demo:latest
```

Then visit http://localhost:5000

## Run Locally From Source

```bash
git clone https://github.com/haseebspaniard/docker-ghcr-demo.git
cd docker-ghcr-demo
docker build -t docker-ghcr-demo:local .
docker run -d -p 5000:5000 docker-ghcr-demo:local
```

## Dockerfile Design Notes

requirements.txt is copied and installed **before** the rest of the application code. This orders the Docker layer cache so dependency installation is only re-run when requirements.txt actually changes — not on every code edit — significantly speeding up rebuilds.

## Debugging Log (Real Issues Hit While Building This)

1. **Workflow silently not running** — GitHub Actions only recognizes workflow files inside .github/workflows/. An early version of docker-publish.yml was accidentally placed in the repo root, which GitHub silently ignored (0 workflow runs, no error message). Fixed by moving the file to the correct path.
2. **Windows Notepad extension trap** — Saving Dockerfile via Notepad silently appended .txt, producing an empty file that Docker couldn't find. Solved by creating files via PowerShell here-strings (Out-File -Encoding utf8 -NoNewline) instead.
3. **Image tag mismatch** — docker/metadata-action with a semver pattern strips the leading v from release tags. Releasing v1.0.1 produced a Docker image tagged 1.0.1, not v1.0.1 — this is standard Docker/OCI convention, not a bug.

## Author

**Abdul Haseeb** — Former CS/ICT teacher transitioning into Cloud & DevOps Engineering.
[GitHub](https://github.com/haseebspaniard) · [LinkedIn](https://www.linkedin.com/in/abdulhaseebas) · [Medium](https://medium.com/@haseebabdul480)
