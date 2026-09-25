# Session 001 — Python Environment & Virtual Environment Setup

## Status: 🟢 Completed (Approved 2026-09-24)

---

## Objective

Set up Python 3.11+ and create an isolated virtual environment for the Smart Crop Assistant backend.

## Why

Every professional Python project runs inside an isolated virtual environment. Without isolation:
- Installing a package for Project A can break Project B.
- You cannot reproduce the exact dependency set on another machine.
- Deployment becomes unpredictable because the server may have different package versions.

## Concepts Learned

1. **Virtual Environment**: An isolated Python installation inside a `.venv/` folder that keeps project dependencies separate from the system Python and other projects.
2. **Activation**: Temporarily redirects `python` and `pip` commands to the venv copy for the current terminal session.
3. **Isolation Proof**: The `pip --version` path containing `.venv` confirms packages are installed in the project-local environment.
4. **Python 3.12+ Change**: `setuptools` is no longer bundled by default in new virtual environments — environments start leaner.

## Prerequisites

- Python 3.11+ installed ✅ (Python 3.14.7 confirmed)
- VS Code installed ✅
- PowerShell terminal ✅

## Tasks Completed

| Task | Status | Output |
|------|--------|--------|
| Verify Python version | ✅ | Python 3.14.7 |
| Navigate to project directory | ✅ | cd successful |
| Create virtual environment | ✅ | .venv/ folder created |
| Activate virtual environment | ✅ | (.venv) prefix visible in prompt |
| Verify isolation (pip --version) | ✅ | Path confirms .venv location |
| Verify clean environment (pip list) | ✅ | Only pip 26.2.1 listed |
| Upgrade pip | ✅ | Already at latest (26.2.1) |

## Files Created

| File/Directory | Action | Purpose |
|---------------|--------|---------|
| `.venv/` | Created | Isolated Python 3.14.7 virtual environment |

## Testing

| Test | Result |
|------|--------|
| Python executable points to .venv | ✅ Confirmed |
| sys.prefix points to .venv | ✅ Confirmed |
| pip installs to .venv/Lib/site-packages | ✅ Confirmed |
| Environment is isolated (pip list is clean) | ✅ Confirmed |

## Git Actions

Not applicable — Git initialization happens in Session 003.

## Problems Encountered

None.

## Lessons Learned

1. Virtual environments prevent dependency conflicts between projects.
2. The `.venv` prefix convention signals "auto-generated tooling, not source code."
3. Activation only affects the current terminal session — new terminals require re-activation.
4. Modern Python (3.12+) no longer bundles setuptools in venvs by default.
5. Always verify isolation by checking `pip --version` path and `pip list` contents.

## Learning Questions — Can You Answer These?

1. What happens if you install packages globally instead of in a virtual environment?
2. What is the difference between `python -m venv .venv` and `pip install virtualenv`?
3. Why do we name the directory `.venv` with a dot prefix?
4. What does "activating" a virtual environment actually change in your terminal?
5. Why do we upgrade pip immediately after creating a venv?

## Definition of Done

- [x] Python 3.11+ confirmed (3.14.7)
- [x] `.venv/` directory created
- [x] Virtual environment activates successfully
- [x] `pip list` shows only pip (clean environment)
- [x] pip is at latest version (26.2.1)
- [ ] Student confirms understanding of WHY virtual environments are necessary

## Review

Awaiting student approval.
