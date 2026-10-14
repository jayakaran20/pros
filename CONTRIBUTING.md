# Contributing to Cropfit

Thank you for your interest in contributing to **Cropfit**! We welcome contributions from developers, agronomists, data scientists, and ML engineers.

---

## 1. Development Workflow

1. **Fork the Repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/<your-username>/pros.git
   cd pros
   ```
3. **Create a topic branch**:
   ```bash
   git checkout -b feat/your-feature-name
   ```

---

## 2. Local Environment Setup

### Backend:
```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS / Linux

pip install -r backend/requirements.txt
```

### Frontend:
```bash
cd frontend
npm install
```

---

## 3. Quality Standards & Quality Gates

Before submitting a Pull Request, verify that all automated quality gates pass:

1. **Backend Tests & Code Coverage ($\ge 80\%$)**:
   ```bash
   pytest --cov=backend/app --cov-report=term-missing backend/tests/
   ```
2. **Frontend Contract Tests**:
   ```bash
   cd frontend
   npm test
   ```
3. **Frontend Production Compilation**:
   ```bash
   cd frontend
   npm run build
   ```
4. **Automated Smoke Tests**:
   ```bash
   python backend/scripts/smoke_test.py
   ```

---

## 4. Conventional Commits

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
* `feat`: A new user-facing feature.
* `fix`: A bug fix.
* `docs`: Documentation changes.
* `test`: Adding or updating test cases.
* `chore`: Maintenance, dependencies, or configuration updates.
* `ci`: CI/CD pipeline modifications.

---

## 5. Submitting a Pull Request

1. Push your branch to GitHub:
   ```bash
   git push origin feat/your-feature-name
   ```
2. Open a Pull Request against the `main` branch.
3. Verify that all 3 GitHub Actions CI checks turn green!
