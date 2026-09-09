## Context

See proposal.md — Why. Two constraints shape the approach beyond that.

First, the packaging change has a wider blast radius than `setup.py` itself. Removing
`setup.py` breaks `.github/workflows/python-publish.yml`, which builds releases with
`python setup.py sdist bdist_wheel`. Raising the Python floor contradicts
`.readthedocs.yaml`, which pins `python: "3.8"` on `ubuntu-20.04`, and `docs/requirements.txt`,
which pins Sphinx 3.5.4 from 2021. All three have to move together or the first release or
docs build after this lands fails.

Second, the repository carries a second, meta-supplied CI workflow (`.github/workflows/ci.yml`)
that gates its Python jobs on the presence of `pyproject.toml`. Adding one switches those
jobs from empty passes to real runs, so this change is also the moment their configuration
has to be correct — including the `mypy src` invocation, which names a directory this
project does not have.

## Goals / Non-Goals

**Goals:**

- `render()` works on the newest matplotlib the project permits, in both render modes.
- One `pyproject.toml` is the only place package metadata lives.
- `ruff check`, `ruff format --check` and `mypy` all pass with zero findings, and all three
  actually execute in CI.
- The dependency floors the manifest declares are ones the project is tested against.

**Non-Goals:**

- Migrating to a `src/` layout. The delivered `ci.yml` assumes one, but moving the package
  is churn that changes no behavior and invalidates every existing import path in notebooks
  and downstream code. The one CI line is what changes instead.
- `mypy --strict`. Chosen against deliberately; see Decisions.
- Any change to simulation dynamics, observations, rewards, or registered scenario ids.
  This change must be behavior-preserving apart from the render fixes and the new metadata
  entry.
- Rewriting the notebooks in `examples/`. They are checked separately and are not part of
  the quality gates.

## Decisions

**Python floor at 3.10, not 3.9 or 3.8.**
numpy 2.x requires 3.10, and numpy 2 is what current matplotlib and gymnasium are built
against. Holding at 3.9 would pin numpy below 2 indefinitely and leave the project on a
matplotlib old enough to still have the removed APIs — solving the symptom while keeping the
cause. 3.8 has been EOL since October 2024. Alternative considered: keep 3.8 and shim the
two matplotlib calls with `hasattr` checks. Rejected because it preserves a dependency floor
that blocks every future upgrade, and because the CI matrix would keep paying for four
interpreters to test a configuration nobody installs.

**ruff replaces black, flake8 and isort; not added alongside them.**
Running both is a standing source of disagreement over formatting. `ruff format` is
black-compatible, so the formatting outcome is nearly unchanged, and `ruff check` covers the
flake8 and isort rule sets already in use. Alternative considered: ruff for linting only,
keeping black for formatting. Rejected — two tools, two pinned versions, no benefit.

**mypy at default settings, not `--strict`.**
The 29 current errors include real defects worth fixing: `Movement` and `Arrival` annotate
`self.rng` as `None` and then call `.uniform()` on it, and `Channel.isoline` constructs a
`UserEquipment` with a `None` id purely as a probe object. Default settings surface exactly
those. `--strict` would additionally demand annotations on every function body and force
casts around numpy and gymnasium generics, producing a large diff dominated by noise in
which the real fixes would be hard to review. The gate can be tightened later once the
signal-to-noise ratio is better.

**Fix the two matplotlib calls with their documented replacements, not a compatibility shim.**
`cm.get_cmap("RdYlGn")` becomes `matplotlib.colormaps["RdYlGn"]`, and
`canvas.tostring_rgb()` becomes a slice of `canvas.buffer_rgba()` dropping the alpha
channel. Both replacements exist well below the matplotlib floor this change sets, so no
version branching is needed. The `human` render path already uses `buffer_rgba`, so the two
paths converge on one API.

**Normalize line endings to LF, repository-wide, in its own commit.**
`mobile_env/core/schedules.py` and `mobile_env/handlers/central.py` are stored CRLF while
the rest of the tree is LF. `ruff format` will normalize them, which would bury a two-line
change inside a whole-file diff. Doing the normalization as a separate, reviewable commit
and recording `* text=auto` in `.gitattributes` keeps the substantive commits readable.

**Move `ray[rllib]` to an optional extra rather than a runtime dependency.**
`mobile_env/wrappers/multi_agent.py` imports `ray` at module scope but `ray` is in neither
`requirements.txt` nor `setup.py`. It works today only because `wrappers/__init__.py` is
empty, so nothing imports the module unless a user asks for it. Declaring an `rllib` extra
makes that contract explicit without adding a heavy dependency to every install.

**Rename one of the two workflows named `CI`.**
`ci.yml` and `python-package.yml` both declare `name: CI`, so `gh pr checks` and the branch
protection UI cannot distinguish them. `python-package.yml` — the matrix build — is renamed
to make the pair legible. Alternative considered: merge the two workflows. Rejected for now:
`ci.yml` is meta-supplied and is overwritten by the next broadcast, so local edits to it
should stay minimal.

## Risks / Trade-offs

**Dropping Python 3.8 and 3.9 is breaking for existing users** → It is a declared floor in
package metadata, so pip refuses the install rather than failing at import; the change ships
as a minor version bump with the floor stated in the README installation section.

**Removing `setup.py` breaks the release workflow silently** → Nothing fails until the next
release is cut, which is the worst time to find out. `python-publish.yml` is converted to
`python -m build` in the same change, and the build is exercised in CI so a broken manifest
fails on a pull request rather than at release time.

**Bumping the docs toolchain may change rendered output** → Sphinx 3.5.4 to a current
version is a four-year jump. The docs build is verified locally before merge; any theme or
directive breakage is fixed as part of this change rather than deferred.

**`ci.yml` is meta-supplied and will be re-delivered** → The `mypy src` fix is a local edit
to a file the next broadcast may overwrite, silently reverting it. Recorded as feedback via
`/alemax:feedback` so the meta side can carry the fix, and the local edit is kept to the one
line so a future conflict is trivial to resolve.

**A clean mypy pass can be achieved by weakening types rather than fixing code** → The
annotation changes are reviewed for whether they describe what the code does; the
`self.rng` and `isoline` cases are fixed at the source rather than annotated away.

## Open Questions

- Whether `python-package.yml` should keep testing three operating systems once `ci.yml`'s
  jobs are actually running. Deferred: it does not change what gets built here, only how
  long CI takes, and is easy to trim later.
