## Purpose

Defines the Gymnasium-compatible control loop the environment exposes to any agent or framework: how an episode is created, reset, stepped, terminated and closed, and what an agent receives back at each step.

## Requirements

### Requirement: Gymnasium API conformance
The environment SHALL implement the Gymnasium `Env` interface so that any Gymnasium-compatible framework can drive it without adaptation.

#### Scenario: Standard Gymnasium API check passes
- **WHEN** a registered environment is created and submitted to a Gymnasium API conformance checker
- **THEN** the checker reports no violation of the `reset`/`step`/`render`/`close` contract, and the declared `action_space` and `observation_space` match the values actually returned

#### Scenario: Spaces are provided by the control handler
- **WHEN** an environment is constructed
- **THEN** `action_space` and `observation_space` are the spaces reported by the configured control handler for that environment

### Requirement: Episode reset
`reset` SHALL return the initial observation and info dictionary and SHALL restore every part of the simulation to a fresh episode state.

#### Scenario: Reset returns observation and info
- **WHEN** `reset()` is called
- **THEN** it returns a `(observation, info)` pair, the simulation time is `0`, no connections are established, and each user equipment has a freshly drawn arrival time, departure time and initial position

#### Scenario: Reset with an explicit seed
- **WHEN** `reset(seed=<value>)` is called
- **THEN** the seed is applied to the environment and its models before the episode is generated

#### Scenario: Extra reset options are rejected
- **WHEN** `reset(options=<anything not None>)` is called
- **THEN** the call raises `NotImplementedError` rather than silently ignoring the options

### Requirement: Environment step
`step` SHALL apply the agent's action, advance the simulation by one time step, and return the five-tuple `(observation, reward, terminated, truncated, info)`.

#### Scenario: A step advances the simulation
- **WHEN** `step(action)` is called on a running episode
- **THEN** connections are updated, data rates and utilities are recomputed, active users move, the internal time advances by one, and the tuple `(observation, reward, terminated, truncated, info)` is returned

#### Scenario: Stepping a finished episode is refused
- **WHEN** `step()` is called after the episode has already ended
- **THEN** the call fails with an assertion rather than producing another transition

### Requirement: Episode termination by time limit only
The environment SHALL have no natural terminal state: an episode SHALL end only by truncation, once the configured episode time limit is reached or the last user equipment has departed, whichever comes first.

#### Scenario: Episode runs to the time limit
- **WHEN** an episode is stepped repeatedly with arbitrary actions
- **THEN** `terminated` is `False` at every step, and `truncated` becomes `True` on the step at which simulation time reaches the smaller of the configured maximum episode time and the last departure time

#### Scenario: Visualization is released at episode end
- **WHEN** the episode ends while a rendering window is open
- **THEN** the environment closes that window

### Requirement: Steps with no active users are skipped
When no user equipment is requesting service and the episode has not ended, the environment SHALL advance time on its own rather than asking the agent for an action it cannot meaningfully take.

#### Scenario: Time skips ahead to the next active user
- **WHEN** a step leaves no active user equipment and the episode time limit has not been reached
- **THEN** the environment continues stepping internally until at least one user equipment is active or the episode ends, and only then returns to the caller

### Requirement: Step information dictionary
The `info` dictionary returned by `reset` and `step` SHALL combine the control handler's information with the latest value of every tracked metric.

#### Scenario: Info carries handler and metric entries
- **WHEN** `step()` returns
- **THEN** `info` contains the handler's own entries merged with the most recent value of each scalar, per-user and per-station metric registered with the monitor

### Requirement: Deterministic runs from a seed
Given the same configuration and seed, the environment SHALL produce the same episode.

#### Scenario: Same seed reproduces an episode
- **WHEN** two environments are built from the same configuration and seed and stepped with the same actions
- **THEN** they produce identical observations, rewards and info at every step

#### Scenario: Random streams may persist across episodes
- **WHEN** `reset_rng_episode` is disabled
- **THEN** the random streams of the arrival, movement and other models continue across episodes instead of restarting, so successive episodes differ

### Requirement: Environment shutdown
`close` SHALL release visualization resources and SHALL be safe to call more than once.

#### Scenario: Closing stops rendering
- **WHEN** `close()` is called
- **THEN** any open window is destroyed and later `render()` calls return without drawing
