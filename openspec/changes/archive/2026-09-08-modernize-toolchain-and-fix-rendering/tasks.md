## 1. Line-ending normalization (isolated first, so later diffs stay readable)

- [x] 1.1 Add `* text=auto` to `.gitattributes`; verify `git check-attr text -- mobile_env/core/schedules.py` reports `text: auto`
- [x] 1.2 Convert the two CRLF files (`mobile_env/core/schedules.py`, `mobile_env/handlers/central.py`) to LF and commit alone; verify `file mobile_env/**/*.py | grep -c CRLF` returns 0 and `git show --stat` touches only those two files

## 2. Packaging: pyproject.toml as the single manifest

- [x] 2.1 Write `pyproject.toml` with PEP 621 metadata (name, version 2.1.0, description, readme, license, authors, urls, classifiers) and `requires-python = ">=3.10"`; verify `python -m build` produces a wheel and sdist
- [x] 2.2 Declare runtime dependencies with floors the project is tested against (gymnasium, matplotlib>=3.9, numpy>=2, pandas, pygame, shapely, svgpath2mpl); verify a wheel installed into a clean venv can create and step `mobile-small-central-v0`
- [x] 2.3 Declare optional extras: `test` (pytest, sb3-contrib), `docs` (current sphinx, sphinx-rtd-theme, myst-parser), `rllib` (ray[rllib]); verify `pip install .` alone does not pull ray
- [x] 2.4 Add `[tool.ruff]`, `[tool.mypy]` and `[tool.pytest.ini_options]` sections; verify `ruff check`, `mypy` and `pytest` each pick up config with no CLI flags
- [x] 2.5 Delete `setup.py`, `setup.cfg`, `requirements.txt` and `tests/requirements.txt`; verify `git grep -l "setup.py\|requirements.txt"` returns only intended references (docs, README)
- [x] 2.6 Generate and commit `uv.lock`; verify `uv sync --locked` succeeds and `uv sync --locked` after an unrelated manifest edit fails as designed

## 3. Fix the rendering breakage

- [x] 3.1 Replace `cm.get_cmap("RdYlGn")` in `render_simulation` with `matplotlib.colormaps["RdYlGn"]`; verify `render()` no longer raises `AttributeError` on matplotlib 3.11
- [x] 3.2 Replace `canvas.tostring_rgb()` in `render` with an alpha-dropped slice of `canvas.buffer_rgba()`; verify `rgb_array` mode returns an array of shape `(H, W, 3)` and dtype `uint8`
- [x] 3.3 Add `render_fps` to `MComCore.metadata`; verify a gymnasium `make(..., render_mode="rgb_array")` emits no "No render fps was declared" warning
- [x] 3.4 Confirm both render modes end to end: `rgb_array` returns a frame, and `human` opens and closes a pygame window without error on macOS

## 4. Bring the tree to a clean ruff pass

- [x] 4.1 Apply `ruff check --fix` for the 59 auto-fixable findings (mostly `UP006`/`UP035` PEP 585 annotations, `PIE790`); verify `git diff` shows no behavior change and `pytest` still passes
- [x] 4.2 Fix the remaining findings by hand: `B006` mutable `config={}` defaults (4), `RUF012` mutable class attributes (3), `C403`/`C401` comprehensions, `RUF059` unused unpacked variables, `SIM210`, 2 unused imports; verify `ruff check` reports zero
- [x] 4.3 Run `ruff format` across the tree; verify `ruff format --check` is clean and the diff is confined to formatting

## 5. Bring the tree to a clean mypy pass

- [x] 5.1 Fix `Movement.rng` and `Arrival.rng` being annotated `None` then used as a generator — type them as `np.random.Generator | None` and narrow, or initialize eagerly; verify the 4 `attr-defined` errors in `movement.py` and the `arrival.py` assignment error clear
- [x] 5.2 Fix `Channel.isoline` constructing `UserEquipment(None, **ue_config)` — the id is a probe placeholder; verify the `arg-type` error clears without changing isoline output (compare arrays before and after)
- [x] 5.3 Fix the numpy/array assignment mismatches in `channels.py`, `base.py` (`station_utilities` return type, the `features()` locals) and `handlers/multi_agent.py` observation dict typing; verify each named error clears
- [x] 5.4 Fix `wrappers/multi_agent.py` `step` returning a 5-tuple against a 4-tuple annotation; verify the `return-value` error clears and the RLlib contract in the spec still holds
- [x] 5.5 Verify `mypy mobile_env` reports zero errors at the settings committed in `pyproject.toml`

## 6. Wire the gates into the dev loop and CI

- [x] 6.1 Replace black, flake8 and isort with `ruff` and `ruff-format` in `.pre-commit-config.yaml`; verify `pre-commit run --all-files` passes from a clean checkout
- [x] 6.2 Change `ci.yml`'s type-check step from `mypy src` to the real package path; verify the type-check job runs instead of failing on a missing directory
- [x] 6.3 Retarget `python-package.yml` to Python 3.10-3.13 and rename it so it no longer collides with `ci.yml`'s `name: CI`; verify `gh pr checks` lists two distinguishable workflows
- [x] 6.4 Convert `python-publish.yml` from `python setup.py sdist bdist_wheel` to `python -m build`; verify the build step succeeds on a workflow_dispatch dry run or an equivalent local `python -m build`
- [x] 6.5 Bump `.readthedocs.yaml` off Python 3.8 and `ubuntu-20.04`, and point it at the `docs` extra instead of `docs/requirements.txt`; verify a local `sphinx-build docs docs/_build` succeeds on the new toolchain

## 7. Documentation and close-out

- [x] 7.1 State the Python floor in `README.md`'s installation section and drop the `pip install -r requirements.txt` equivalence claim; verify no README command references a deleted file
- [x] 7.2 Confirm CI is green on the pull request with lint, type-check and test all having actually executed — check the job logs, not just the check marks, since these jobs previously passed while running nothing
- [x] 7.3 File `/alemax:feedback` recording that `ci.yml`'s `mypy src` path assumes a src layout, so the meta side can carry the fix rather than re-delivering it
- [x] 7.4 After archiving, add the repo's H1 + `## Summary` header to the new `openspec/specs/package-distribution/spec.md`; verify `uv run --script bin/spec-summary-check.py` reports zero warnings
