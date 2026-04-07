# CHEASY

CHEASY is a classroom-oriented culinary learning platform for teachers and students. The current codebase is a full-stack monorepo with a Flask backend, a React frontend, JWT-based auth for the API, and a lightweight admin interface for database inspection and management.

This README is written for developers, not end users. It is meant to answer four questions quickly:

1. What is this repo supposed to do?
2. How is it built?
3. How do I run it in local VS Code, Gitpod, or Codespaces?
4. What parts are finished, and what parts are still rough?

## What CHEASY Is

CHEASY models a simple learning platform around culinary instruction.

- Teachers and students can register separately.
- Both roles can log in and receive JWT tokens.
- The backend models courses, sections, assignments, submissions, and enrollments.
- The frontend currently supports auth, static marketing pages, and role-based dashboard routing.
- The backend also exposes a Flask-Admin panel and a custom login-protected dashboard page.

At a high level, this project is part product prototype, part classroom-management backend.

## Tech Stack

### Backend

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Flask-Admin
- SQLite by default
- Pipenv for dependency and script management

### Frontend

- React 19
- React Router 7
- Create React App / react-scripts
- env-cmd for loading the shared root local env file
- Simple flux-style store with React context

### Workspace Tooling

- VS Code automatic tasks for local startup
- Gitpod workspace startup via `.gitpod.yml`
- GitHub Codespaces / devcontainers via `.devcontainer/devcontainer.json`

## Repository Layout

```text
.
├── backend/
│   ├── app.py              # Flask app entrypoint
│   ├── routes.py           # JSON API routes
│   ├── models.py           # SQLAlchemy models
│   ├── dashboard.py        # Simple backend dashboard/login pages
│   ├── admin.py            # Flask-Admin setup
│   ├── seed.py             # Development seed data
│   ├── Pipfile             # Backend dependency definition
│   └── instance/           # Local SQLite and instance data
├── frontend/
│   ├── package.json        # Frontend scripts and dependencies
│   ├── public/             # Static public assets
│   └── src/
│       ├── index.js        # React entrypoint
│       ├── js/
│       │   ├── Layout.js   # Top-level routes and nav
│       │   ├── flux/       # Session store and app context
│       │   └── pages/      # Home, About, Auth, Dashboard pages
│       └── styles/
├── .env.example            # Safe template for local environment config
├── .vscode/                # VS Code tasks/settings
├── .gitpod.yml             # Gitpod setup
└── .devcontainer/          # Codespaces/devcontainer setup
```

## Architecture Overview

### Backend flow

- `backend/app.py` creates the Flask app, loads the root environment file, initializes extensions, creates tables on startup, registers the JSON API blueprint, and registers the admin/dashboard views.
- `backend/models.py` defines the core domain models.
- `backend/routes.py` exposes authentication and CRUD endpoints.
- `backend/admin.py` wires Flask-Admin model views.
- `backend/dashboard.py` provides a basic password-protected HTML dashboard separate from the React frontend.
- `backend/seed.py` resets and repopulates the database with development data.

### Frontend flow

- `frontend/src/index.js` wraps the app with `StoreProvider` and `BrowserRouter`.
- `frontend/src/js/flux/store.js` manages session state, localStorage persistence, login, register, and logout actions.
- `frontend/src/js/Layout.js` handles navigation and role-based dashboard routing.
- `frontend/src/js/pages/Auth.js` is the most connected UI path today. It talks to the backend login and register endpoints.
- `frontend/src/js/pages/Dashboard.js` is currently mock-data UI, not API-backed dashboard logic.

## Domain Model

The backend domain currently revolves around these entities:

- `Teacher`
- `Student`
- `Course`
- `Section`
- `Assignment`
- `Submission`
- `Enrollment`

Conceptually, the relationships are intended to look like this:

- A `Course` has many `Section`s.
- A `Section` has many `Assignment`s.
- A `Student` submits work for an `Assignment` through `Submission`.
- A `Teacher`, `Student`, and `Course` are linked through `Enrollment`.

Important current-state note:

The codebase contains schema mismatches between `backend/models.py`, `backend/routes.py`, and `backend/seed.py`. For example, `Assignment` is modeled with `section_id` in the ORM, while some route and seed logic still behaves as if assignments belong directly to courses. New contributors should expect to reconcile this before expanding assignment features.

## Current Feature Status

### Working or mostly working

- Teacher login endpoint
- Student login endpoint
- Teacher registration endpoint
- Student registration endpoint
- JWT-protected CRUD patterns for most resources
- Flask app startup with automatic table creation
- Flask-Admin panel exposure
- Local session persistence in the React frontend
- Seed script for development data
- Workspace startup support for VS Code, Gitpod, and Codespaces

### Partial or prototype-level

- Frontend dashboards are mock-data components
- Backend HTML dashboard contains stale copy from an older API shape
- Some backend route logic does not fully match the current models
- Route protection exists, but role-based authorization rules are still minimal
- local environment configuration is shared across frontend and backend, which is practical for development but should be handled more carefully for production

## Local Configuration

This project expects a root `.env` file for local development, but that file should not be committed.

Use `.env.example` as the template:

```bash
cp .env.example .env
```

Then adjust the values in `.env` for your machine or cloud workspace.

General rule:

- local development should usually use localhost URLs
- Codespaces and Gitpod may need their preview URLs instead
- secrets should stay only in `.env`, never in the README and never in git

If the frontend is talking to the wrong backend, the first thing to check is whether `.env` still points at an old preview URL.

## Local Development

### Prerequisites

- Python 3.12
- Node.js 20 or compatible modern Node version
- npm
- Pipenv

### Backend setup

From `backend/`:

```bash
python -m pip install --user pipenv
export PATH="$HOME/.local/bin:$PATH"
pipenv sync
pipenv run python app.py
```

Useful backend commands:

```bash
export PATH="$HOME/.local/bin:$PATH"
pipenv run python seed.py
pipenv run flask db migrate
pipenv run flask db upgrade
```

### Frontend setup

From `frontend/`:

```bash
npm install
npm start
```

The frontend reads the root `.env` file through `env-cmd`.

### Endpoints during local development

- Frontend: `http://localhost:3000`
- Backend API/root: `http://localhost:3001`
- Admin panel: `http://localhost:3001/admin/`
- Backend login page: `http://localhost:3001/admin-login`

## Zero-to-Working by Environment

### VS Code

This repo includes:

- `.vscode/tasks.json`
- `.vscode/settings.json`

Behavior:

- VS Code is configured to allow automatic tasks in the workspace.
- Opening the repo should start two tasks on folder open:
	- backend: `pipenv run python app.py`
	- frontend: `npm start`
- Two manual setup tasks also exist if dependencies are not installed yet.

If the startup tasks fail on a clean machine, run the dependency setup tasks once, then reopen the workspace.

### Gitpod

`.gitpod.yml` will:

- install Pipenv and sync backend dependencies
- install frontend npm dependencies
- start backend and frontend in separate terminals
- expose ports `3000` and `3001`

### GitHub Codespaces

`.devcontainer/devcontainer.json` will:

- provision a Python 3.12 dev container
- add Node 20
- install backend dependencies with Pipenv
- install frontend dependencies with npm
- forward ports `3000` and `3001`
- apply the same automatic VS Code task setting used locally

This is the best-supported cloud environment after Gitpod.

## Authentication Model

The API currently supports separate teacher and student login flows.

Public auth endpoints:

- `POST /api/teacher/login`
- `POST /api/student/login`
- `POST /api/teachers`
- `POST /api/students`

After login, the backend returns a JWT access token. The frontend stores:

- `token`
- `role`
- `username`

in localStorage and rehydrates that session on refresh.

Important note:

JWT authentication is in place, but role-specific authorization is still light. A valid token is the main protection layer on most CRUD endpoints today.

## API Surface

The backend exposes CRUD-style routes for:

- teachers
- students
- courses
- sections
- assignments
- submissions
- enrollments

Most non-auth routes require JWTs via `@jwt_required()`.

Because parts of the route layer still reflect earlier schema assumptions, treat the API as evolving rather than locked.

## Seed Data

The seed script is designed for development, not production.

Run:

```bash
cd backend
export PATH="$HOME/.local/bin:$PATH"
pipenv run python seed.py
```

What it does:

- creates tables if needed
- clears existing data
- creates teachers, students, courses, sections, assignments, enrollments, and submissions

Seeded teacher accounts:

- `chefmarco` / `password123`
- `chefana` / `securepass456`

Seeded student accounts:

- `alice` / `password123`
- `bob` / `securepass456`
- `charlie` / `mypassword789`

These credentials are for development only.

## Admin and Operations

There are two backend-facing HTML surfaces outside the React app:

### Flask-Admin

- URL: `/admin/`
- Purpose: direct inspection and editing of SQLAlchemy-backed models

### Custom backend login/dashboard

- URL: `/admin-login`
- Purpose: password-protected landing page for backend links

Important note:

The custom dashboard template still references stale endpoints from an older project shape. Do not assume that page is authoritative documentation for the current API.

## Known Issues and Developer Caveats

This section matters. A new developer should read it before building on top of the current code.

### Backend inconsistencies

- `Assignment` in the ORM uses `section_id`, but some route and seed logic still expects a course-level assignment relationship.
- `Section.description` is required in the model, but the create/update route logic does not consistently populate it.
- The backend HTML dashboard still documents endpoints that no longer match the current teacher/student/course schema.

### Frontend limitations

- Dashboard pages are static mock UIs and are not yet wired to backend resources.
- Auth is the main connected workflow today.
- Some navigation and imagery assume local static assets exist in `public/`.

### Security posture

- local secrets live in `.env`, which is now gitignored.
- Admin auth is cookie/password-based and lightweight.
- This repo is suitable for development and prototyping, not production deployment in its current state.

## Suggested Development Priorities

If you are continuing work on CHEASY, the highest-value cleanup path is probably:

1. Reconcile the ORM schema with route and seed logic.
2. Replace dashboard mock data with API-backed teacher and student views.
3. Tighten authorization rules so teachers and students only access role-appropriate resources.
4. Split development-only config from deployable environment configuration.
5. Add automated tests around auth and the core resource routes.

## Quick Start Checklist

If you only need the shortest path to a running workspace:

1. Copy `.env.example` to `.env` and set the correct values for your environment.
2. Start the backend from `backend/` with `pipenv run python app.py`.
3. Start the frontend from `frontend/` with `npm start`.
4. Optionally seed the database with `pipenv run python seed.py`.
5. Log in with one of the seeded accounts.

## Contribution Notes

When making backend changes, update these areas together if the domain model changes:

- `backend/models.py`
- `backend/routes.py`
- `backend/seed.py`
- any frontend pages that assume a specific API shape

If you change environment assumptions, also review:

- `.env.example`
- `.vscode/tasks.json`
- `.gitpod.yml`
- `.devcontainer/devcontainer.json`

That keeps local, Gitpod, and Codespaces startup behavior aligned.