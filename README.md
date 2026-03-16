# Dockerized Healthcare Planning Assistant

Healthcare Planning Assistant is a FastAPI-based web application that lets users enter their symptoms and receive **structured, LLM-generated healthcare planning advice**.  
It uses **LangChain** to orchestrate between **Google Gemini** and **Groq Llama** models.

> **Disclaimer:** This tool provides general informational guidance only and is **not** a substitute for professional medical advice, diagnosis, or treatment.

## Features

- FastAPI backend with clean modular structure
- LangChain orchestration with:
  - Google Gemini API
  - Groq Llama API
- Bootstrap-based web UI rendered via Jinja templates
- Environment-based configuration via `python-dotenv`
- Structured output in four sections:
  1. Possible Conditions
  2. Precautions
  3. Medication Guidance
  4. Nutrition Advice

## Project Structure (high level)

- `app/`
  - `main.py` – FastAPI app factory and routing setup
  - `core/config.py` – configuration (`pydantic` + `python-dotenv`)
  - `api/routes_symptoms.py` – web routes for form and analysis
  - `models/api/schemas.py` – Pydantic request/response models
  - `services/llm/` – LangChain-based LLM clients and orchestrator
  - `templates/` – Jinja2 templates (`base.html`, `index.html`)
  - `static/` – CSS/JS assets

## Prerequisites

- Python 3.10+ recommended
- Valid API keys for:
  - Google Gemini
  - Groq (Llama models)

## Setup Instructions

1. **Clone or create the project**

   ```bash
   cd "c:\Users\Meet Solanki\OneDrive\Desktop\Projects\Dockerized Healthcare"
   ```

2. **Create and activate a virtual environment (recommended)**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # on Windows PowerShell
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   - Copy `.env.example` to `.env`:

     ```bash
     copy .env.example .env
     ```

   - Open `.env` and set:
     - `GEMINI_API_KEY`
     - `GROQ_API_KEY`
     - (optional) `GEMINI_MODEL`, `GROQ_MODEL`, `DEFAULT_MODEL`

5. **Run the application**

   From the project root:

   ```bash
   uvicorn app.main:app --reload
   ```

   By default this will start the server at `http://127.0.0.1:8000`.

6. **Use the web interface**

   - Open `http://127.0.0.1:8000/` in your browser.
   - Enter your symptoms in the text area.
   - (Optionally) provide age, sex, and duration.
   - Choose the LLM model (Google Gemini or Groq Llama).
   - Click **Generate advice**.
   - The page will render four cards:
     - Possible Conditions
     - Precautions
     - Medication Guidance
     - Nutrition Advice

## Containerized Deployment

This project includes a **multi-stage Dockerfile** and `docker-compose.yml` for containerized deployment and later CI/CD / Kubernetes integration.

### Build the Docker image

From the project root:

```bash
docker build -t healthcare-planning-assistant .
```

### Run the container with docker run

Make sure you have a `.env` file (copied from `.env.example`) with your API keys set.

```bash
docker run --rm -p 8000:8000 --env-file .env healthcare-planning-assistant
```

Then open:

- `http://127.0.0.1:8000/` – web UI
- `http://127.0.0.1:8000/health` – health check endpoint

### Run with docker-compose

```bash
docker-compose up --build
```

This:

- Builds the image.
- Starts the app service on port `8000`.
- Injects environment variables from `.env`.
- Adds a container-level health check hitting `/health`.

### CI/CD and Kubernetes readiness

- The `Dockerfile` produces a small, production-ready Python image using a multi-stage build and a non-root user.
- `docker-compose.yml` can be adapted into Kubernetes manifests (Deployment + Service + livenessProbe using `/health`).
- CI/CD pipelines can:
  - Run tests.
  - Build the Docker image with `docker build`.
  - Push to a registry.
  - Deploy to Kubernetes using the same container image and environment variables.

## Error Handling

- If symptoms are missing or invalid, the form re-renders with an error message.
- If the selected LLM provider is misconfigured (e.g., missing API key), the UI displays a clear error.
- Generic failures when calling the LLM APIs return a user-friendly error and do not expose internal details.

## Notes

- This project is designed to be **Docker-friendly**; configuration is fully driven by environment variables.
- You can later add more routes, models, or persistence (e.g., PostgreSQL) without changing the existing LLM orchestration.
=======
# Dockerized Healthcare Service

**Group No: D6 - Group 11**

**Project No:** DO-22
---

## Project Description

This project focuses on building and deploying a **Healthcare Web Service using Python**. The application is containerized using **Docker** to ensure consistent and portable deployment across different environments.By using Docker, the healthcare service can run reliably without dependency conflicts, making the system easier to deploy, scale, and manage. The project demonstrates how modern DevOps practices can be used to deploy web services efficiently.

---

## Project Overview

The system provides a simple healthcare service API , which can handle basic healthcare-related operations such as patient information management or service responses The application is packaged inside a **Docker container**, allowing developers to run the service in any environment without manually installing dependencies.

---

## Objectives

• **Automation:** To deploy the healthcare Flask application using Docker containers instead of manual environment setup.

• **Consistency:** To ensure the application runs the same way across development and deployment environments.

• **Portability:** To allow the healthcare service to run on any system that supports Docker without dependency issues.

• **Scalability:** To make it easier to scale the healthcare service by running multiple container instances when needed.

• **Reliability:** To improve application reliability by packaging all dependencies within a Docker container.

---

## Tech Stack

| Category | Tools/Technologies Used |
|----------|--------------------------|
| IaC & Orchestration | Terraform, Kubernetes (K8s), Docker |
| CI/CD & Automation | GitHub Actions, Git |
| Backend (Control Plane) | Node.js, Express.js |
| Database & Auth | MongoDB (Mongoose), JWT, Bcrypt |
| Frontend/Templating | EJS (Embedded JavaScript) |
| Environment Mgmt | Dotenv, Cookie-parser, Multer |

---

## Key Features

• **Containerized Deployment:** The healthcare Flask application is packaged into Docker containers for consistent and portable execution.

• **RESTful API Service:** Provides API endpoints for healthcare-related operations using the Flask framework.

• **Environment Consistency:** Docker ensures the application runs the same across development and deployment environments.

• **Simplified Setup:** All application dependencies are bundled within the container, eliminating manual installation.

• **Scalable Architecture:** The containerized setup allows the service to be easily scaled when required.

---

## Group Members

1. Mayuri Patidar – EN22CS301593  
2. Meet Solanki – EN22CS301595  
3. Mokshika Yadav – EN22CS301614  
4. Nirdesh Sharma – EN22CS301655  
5. Palak Shahdadpuri – EN22CS301677  
6. Pankaj – EN22CS301679

---

## Conclusion

The Dockerized Healthcare Python Flask Service demonstrates the importance of containerization in modern application deployment. By moving away from manual environment setup to container-based deployment using Docker, the project ensures a consistent, reliable, and portable application environment. This approach significantly reduces dependency conflicts and simplifies the deployment process. The project serves as a foundation for building scalable and easily deployable healthcare web services that can run efficiently across different platforms with minimal configuration.

>>>>>>> 3505c5be6677d12a6fda916b3d7a031ef6cd14b4

