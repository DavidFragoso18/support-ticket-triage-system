# Contributing to Support Ticket Triage System

Thanks for your interest in contributing! This document explains how to set up a local environment, run checks, and open pull requests.

## Local Development Setup (Python)

The repo is currently language-agnostic, but we standardize Python tooling for linting/formatting. To work with Python code locally:

1. Create and activate a virtual environment
   - PowerShell (Windows):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - Bash (macOS/Linux):
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

2. Install development dependencies
   ```powershell
   python -m pip install --upgrade pip
   pip install black ruff pre-commit pytest
   ```

3. (Optional but recommended) Install pre-commit hooks
   ```powershell
   pre-commit install
   ```
   This will automatically run formatters and linters on each commit.

## Common Tasks

- Format code with Black
  ```powershell
  black .
  ```

- Lint with Ruff
  ```powershell
  ruff check .
  ```
  Auto-fix where possible:
  ```powershell
  ruff check . --fix
  ```

- Run tests (if/when tests exist)
  ```powershell
  pytest -q
  ```
  Run a single test file:
  ```powershell
  pytest tests/test_example.py -q
  ```

## Pull Request Workflow

1. Create a feature branch from the default branch (e.g., `master` or `main`).
2. Make changes and keep commits focused.
3. Run format, lint, and tests locally:
   ```powershell
   black .
   ruff check .
   pytest -q
   ```
4. Push your branch and open a Pull Request.
5. Ensure PR description clearly states the problem, solution, and any trade-offs.
6. Address review feedback and keep PRs up to date with the target branch when needed.

## Code Style

- Python formatting is enforced with Black (88 char line length by default).
- Python linting is enforced with Ruff (select error/warning rules; see pyproject.toml).
- Prefer small, cohesive modules and functions with clear names.
- Add or update tests when you change behavior.

## Pre-Commit Hooks

- Hooks are configured in `.pre-commit-config.yaml`.
- After `pre-commit install`, the following run on commit:
  - `black` (format)
  - `ruff` (lint)
  - Trailing whitespace and EOF fixers

If you run into issues with hooks, you can run them manually on all files:
```powershell
pre-commit run --all-files
```

