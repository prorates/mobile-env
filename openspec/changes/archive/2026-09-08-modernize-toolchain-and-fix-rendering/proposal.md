## Why

`render()` is broken against any currently installable matplotlib. `cm.get_cmap` was
removed in matplotlib 3.9 and `FigureCanvasAgg.tostring_rgb()` in 3.10, so on a fresh
install — verified here on macOS arm64 with matplotlib 3.11, numpy 2.5, gymnasium 1.3 —
every `render()` call raises `AttributeError`. Stepping still works, so the failure is
invisible until a user tries to visualize or record an episode, which is one of the
project's headline features and the subject of both Colab notebooks.

The project cannot adopt those newer versions anyway: it declares `python_requires=">=3.8"`,
and Python 3.8 has been end-of-life since October 2024 while numpy 2.x requires 3.10+. The
packaging is pre-PEP-621 (`setup.py` plus a `setup.cfg` holding only flake8 config), so
there is no `pyproject.toml` — which also means the repo's CI detects no Python stack and
runs its lint, type-check and test jobs empty, reporting green without executing anything.

Quality tooling is stale in the same way: pre-commit pins black 22.10.0, flake8 6.0.0 and
isort 5.12.0, none of which are run in the job that reports on them. A first ruff pass
reports 95 findings and mypy 29 errors, several of which are real defects rather than
style.

## What Changes

- **BREAKING** Raise the supported Python floor from 3.8 to 3.10. Python 3.8 and 3.9 are
  dropped; the CI matrix retargets to 3.10–3.13.
- Replace `setup.py` and `setup.cfg` with a PEP 621 `pyproject.toml` carrying project
  metadata, runtime dependencies, optional test/doc extras, and tool configuration. Add a
  `uv.lock` so the repo's `uv sync --locked` step resolves.
- Fix the two matplotlib removals so `render()` works on current versions, in both
  `rgb_array` and `human` modes.
- Declare `render_fps` in the environment metadata, which gymnasium currently warns is
  missing.
- Replace black, flake8 and isort with ruff (lint + format) in pre-commit, and bring the
  tree to a clean `ruff check`, `ruff format` and `mypy` pass at default settings. This
  includes fixing the real errors mypy surfaces — models that annotate `self.rng` as `None`
  and then call methods on it, and `Channel.isoline` constructing a `UserEquipment` with a
  `None` id.
- Point the CI type-check job at the real package directory instead of the `src/` path it
  currently names, which does not exist in this project.

Behavior of the simulation itself is unchanged: same dynamics, same observations, same
rewards, same registered scenario ids.

## Capabilities

### New Capabilities

- `package-distribution`: what the published package guarantees to someone installing it —
  which Python versions are supported, what is installed, what importing it does, and that
  its declared dependency set is sufficient to run the environment and its visualization.

### Modified Capabilities

- `visualization`: adds a requirement that the environment declares its render frame rate
  alongside its render modes, so a consumer recording or replaying frames has a stated
  rate rather than having to guess.

## Impact

- **Packaging**: `setup.py` and `setup.cfg` removed; `pyproject.toml` and `uv.lock` added.
  `requirements.txt` and `tests/requirements.txt` become redundant and are folded into
  extras. Anyone installing on Python 3.8 or 3.9 is cut off — a minor version bump.
- **Code**: `mobile_env/core/base.py` (both render fixes, metadata), and typing corrections
  across `core/movement.py`, `core/arrival.py`, `core/channels.py`,
  `handlers/multi_agent.py`, `wrappers/multi_agent.py`.
- **CI**: `.github/workflows/ci.yml` type-check path; `.github/workflows/python-package.yml`
  matrix. Both workflows are currently named `CI`; this change renames one so the two are
  distinguishable.
- **Dev loop**: `.pre-commit-config.yaml` swaps three tools for ruff. Contributors need to
  reinstall hooks.
- **Docs**: `README.md` installation section states the new Python floor.
