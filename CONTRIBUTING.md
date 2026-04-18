# Contributing Guidelines

First of all, thank you for your interest in contributing to the FastAPI JWT Generator & Verifier!

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/getJwt.git
   cd getJwt
   ```

## Development Setup

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   
   # For Windows
   .venv\Scripts\activate
   # For Linux/Mac
   source .venv/bin/activate
   ```
2. **Install all dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
3. **Generate a local `.getJwt` key for testing**:
   ```bash
   ssh-keygen -t ed25519 -f ./getJwt -N "" -q
   ```
   *(Ensure you don't commit your local key pair.)*

## Running Tests

All new features and bug fixes must be backed by tests. We use `pytest` as our testing framework.

Run tests using:
```bash
pytest
```
Ensure that all existing tests pass before submitting your PR.

## Code Structure

The project strictly follows a scalable module structure inside the `app/` folder. Please adhere to this architecture when drafting your PR:

- **`app/api`**: Exclusively contains router logic and path definitions.
- **`app/core`**: Exclusively contains overarching application configurations, utilities, and security logic.
- **`app/schemas`**: Exclusively contains data validation/pydantic models.

## Making a Pull Request 

1. Create a branch for your feature/fix from `main`:
   ```bash
   git checkout -b fix-jwt-error
   ```
2. Make your updates, write tests, and document any changes.
3. Commit your changes logically and with clear messages.
4. Push your branch and open a Pull Request against the `main` branch. 

## Code Style

- Format your code using `black` (if installed) or ensure standard PEP8 compliance.
- Type hints are mandatory. Leverage Pydantic and Python's typing system for functions. 
- Try to make PRs minimal in scope, doing one thing concisely is better than huge refactoring dumps.

Thank you!
