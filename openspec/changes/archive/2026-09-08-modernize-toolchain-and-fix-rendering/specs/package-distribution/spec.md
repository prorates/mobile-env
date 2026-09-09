## Purpose

Defines what the published package guarantees to whoever installs it: which Python interpreters are supported, that a plain install is enough to run the environment and its visualization, and that the repository states a single, checkable source of truth for its metadata and its quality gates.

## ADDED Requirements

### Requirement: Declared supported Python versions
The package SHALL declare the range of Python versions it supports, and an installer SHALL refuse to install it on an interpreter outside that range rather than installing a version that cannot run.

#### Scenario: Supported interpreter
- **WHEN** the package is installed on Python 3.10 or later
- **THEN** the installation succeeds and the environment can be created and stepped

#### Scenario: Unsupported interpreter
- **WHEN** installation is attempted on a Python version below the declared floor
- **THEN** the installer refuses with a version-requirement error instead of installing

### Requirement: A plain install is sufficient to run and to render
The dependencies the package declares SHALL be everything needed to create an environment, step it, and render it — with no extra install step for visualization.

#### Scenario: Stepping after a plain install
- **WHEN** the package is installed with no extras into a clean environment
- **THEN** a registered scenario can be created, reset and stepped to the end of an episode

#### Scenario: Rendering after a plain install
- **WHEN** a registered scenario is created in image-array mode after a plain install
- **THEN** `render()` returns a frame rather than raising, on the dependency versions the package permits

#### Scenario: Optional extras are additive
- **WHEN** a caller installs the package without its test or documentation extras
- **THEN** nothing in the runtime path imports a package supplied only by those extras

### Requirement: Single declarative source of package metadata
The package's name, version, supported Python versions, dependencies and entry points SHALL be declared in one standards-based manifest, so that any compliant build tool produces the same distribution without running project-specific code.

#### Scenario: Building a distribution
- **WHEN** a standards-compliant build front-end builds the project
- **THEN** it produces an installable wheel and source distribution using only the declared metadata

#### Scenario: One place to read the supported versions
- **WHEN** a contributor or a tool needs the supported Python range
- **THEN** it is stated once in that manifest, and the continuous-integration matrix and documentation agree with it

### Requirement: Reproducible development environment
The repository SHALL pin a resolved, committed dependency set so that a contributor and continuous integration install byte-identical versions.

#### Scenario: Locked install
- **WHEN** a contributor or a CI job installs from the committed lock file
- **THEN** the resolved versions match exactly, and the install fails rather than silently re-resolving if the lock is out of date with the manifest

### Requirement: Enforced quality gates
The repository SHALL define lint, formatting, type-check and test gates, SHALL run them in continuous integration against the real package, and a job SHALL NOT report success without having executed its checks.

#### Scenario: Gates run on a change
- **WHEN** continuous integration runs for a pull request
- **THEN** lint, formatting, type-check and tests all execute against the package and the run fails if any of them reports a finding

#### Scenario: A gate that cannot run is not a pass
- **WHEN** a job's checks are skipped because the project does not match what the job expects
- **THEN** that condition is visible rather than being reported as a successful check
