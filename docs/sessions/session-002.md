# Session 002 — VS Code Configuration & Developer Tooling

## Status: ⬜ Planned

---

## Objective

Configure VS Code as a professional Python development environment with automated formatting, linting, type checking, and project settings.

## Why

Writing code without automated tooling leads to:
- **Inconsistent formatting**: Tabs vs spaces, line lengths, import order — causing noisy Git diffs and merge conflicts.
- **Silent bugs**: Unused variables, unreachable code, wrong types — caught only at runtime (or in production).
- **Slow development**: Manually checking style, manually running linters — time better spent engineering.

Professional teams enforce code quality **automatically** via editor configuration. When you press Save, your code is instantly formatted and checked. This session sets up that workflow.

## Concepts to Learn

1. **Linting** — Static analysis that detects code quality issues WITHOUT running the code (unused imports, undefined variables, style violations).
2. **Formatting** — Automatic code style enforcement (indentation, line length, quote style) so all developers produce identical-looking code.
3. **Type Checking** — Verifying that function arguments and return types match their declared types (catches bugs before runtime).
4. **Ruff** — An extremely fast Python linter and formatter (written in Rust) that replaces Black, Flake8, isort, and pyflakes in a single tool.
5. **Mypy** — Python's standard static type checker.
6. **pyproject.toml** — The modern standard configuration file for Python projects (replaces setup.py, setup.cfg, and scattered tool configs).

## Prerequisites

- Session 001 completed ✅
- Virtual environment created and activatable ✅

## Tasks

1. Install VS Code extensions (Ruff, Pylance, Python)
2. Create `.vscode/settings.json` with project-specific configuration
3. Create `pyproject.toml` with Ruff and Mypy configuration
4. Install development dependencies (ruff, mypy) into the virtual environment
5. Verify that formatting and linting work on a test file

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `.vscode/settings.json` | Create | VS Code workspace settings |
| `pyproject.toml` | Create | Project metadata, linter/formatter configuration |

## Testing

- Create a deliberately messy Python file and verify Ruff auto-formats on save
- Create a file with a type error and verify Mypy catches it

## Git Actions

Not yet — Git initialization happens in Session 003.

## Definition of Done

- [ ] Python, Pylance, Ruff extensions installed in VS Code
- [ ] `.vscode/settings.json` configured with format-on-save
- [ ] `pyproject.toml` created with Ruff + Mypy settings
- [ ] `ruff check .` runs without errors
- [ ] `ruff format .` runs without errors
- [ ] Student can explain what linting and type checking are
