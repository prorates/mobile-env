## Purpose

Defines how an episode is measured: the built-in metrics always available to an experimenter, the registration of custom scalar, per-user and per-base-station metrics, and the two ways results are read back — live in the step info dictionary and as tables after the episode.

## Requirements

### Requirement: Metric registration
The environment SHALL accept custom metrics in three categories — scalar, per-user-equipment and per-base-station — each a callable evaluated against the simulation state at every step.

#### Scenario: Registering a custom metric
- **WHEN** a caller registers a named callable in one of the three metric categories through the configuration
- **THEN** that callable is invoked once per step with the simulation state, and its return value is recorded under that name

#### Scenario: Category shapes
- **WHEN** a per-user-equipment or per-base-station metric is evaluated
- **THEN** it returns a mapping keyed by user-equipment or base-station identifier, whereas a scalar metric returns a single value

### Requirement: Built-in metrics
The environment SHALL always track the number of connections, the number of connected user equipments, the mean user data rate and the mean user utility, regardless of what the caller registers.

#### Scenario: Built-ins are present
- **WHEN** an environment is created with an empty metric configuration
- **THEN** those four scalar metrics are still tracked and reported

#### Scenario: Mean over an empty population
- **WHEN** no user equipment has a data rate or a utility yet
- **THEN** the mean data rate is reported as zero and the mean utility as the model's lower utility bound, rather than failing

### Requirement: Metrics are reported live
The latest value of every tracked metric SHALL appear in the info dictionary returned by each step.

#### Scenario: Reading metrics during an episode
- **WHEN** `step()` returns
- **THEN** `info` contains the most recent value of every registered scalar, per-user and per-base-station metric

#### Scenario: Before any step
- **WHEN** `reset()` returns, before any metric has been evaluated
- **THEN** no metric entries are reported rather than empty or placeholder ones

### Requirement: Metrics are recorded for the whole episode
The environment SHALL retain every metric value for the duration of an episode and SHALL make the full history available as tables indexed by time step.

#### Scenario: Reading results after an episode
- **WHEN** the recorded results are loaded
- **THEN** three tables are returned — scalar metrics indexed by time step, per-user metrics indexed by time step and user-equipment identifier, and per-base-station metrics indexed by time step and base-station identifier

#### Scenario: Results are per-episode
- **WHEN** an episode is reset
- **THEN** the recorded history is cleared and a new episode's results start empty
