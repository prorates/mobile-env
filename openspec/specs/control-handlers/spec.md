# Control Handlers

## Summary

A control handler is the strategy object that decides how one simulation is presented to an agent: it fixes the action and observation spaces, interprets incoming actions, selects which features agents see, and computes rewards. The centralized handler exposes the whole network to a single agent as one multi-discrete action and one flat observation vector, rewarded by the mean utility across active user equipments. The multi-agent handler instead gives every user equipment its own observation and its own reward, and that reward deliberately mixes the agent's own utility with the utilities of nearby base stations weighted by how many users they serve, so an agent that overloads a neighbouring cell pays for it. Because a centralized handler encodes a fixed number of users, it refuses at reset any arrival model under which the population changes.

## Purpose

Defines how the same underlying simulation is presented to different kinds of agent: a control handler fixes the action and observation spaces, interprets incoming actions, selects the observations agents see, and computes their rewards, so centralized and multi-agent control share one simulation.

## Requirements

### Requirement: Control handler interface
A control handler SHALL define the action space, the observation space, the transformation of an incoming action into the simulation's per-user form, the observations returned to agents, and the rewards, and SHALL be replaceable by a custom implementation.

#### Scenario: Handler defines the agent-facing contract
- **WHEN** an environment is constructed with a given handler
- **THEN** the environment's action space, observation space, observations, rewards and any extra info entries all come from that handler

#### Scenario: Handler rejects an incompatible configuration
- **WHEN** an episode is reset with a handler that cannot support the configured scenario
- **THEN** the reset fails with an explicit error rather than producing malformed observations

### Requirement: Action encoding
For each user equipment, the action SHALL be a single discrete choice: a no-operation, or one of the base stations to toggle a connection with.

#### Scenario: Action values
- **WHEN** an action is chosen for a user equipment in a network with `N` base stations
- **THEN** the value `0` is the no-operation and the values `1` through `N` select the corresponding base station to connect to or disconnect from

### Requirement: Centralized control
The centralized handler SHALL present the whole network to a single agent that decides for every user equipment in one action, and SHALL reward it with the average quality of experience across active user equipments.

#### Scenario: Centralized action space
- **WHEN** the centralized handler is used
- **THEN** the action space is a multi-discrete space with one entry per user equipment, each ranging over the no-operation and the base stations

#### Scenario: Centralized observation
- **WHEN** the centralized handler produces an observation
- **THEN** it is a single flat vector in `[-1, 1]` concatenating each user equipment's connections, normalized signal-to-noise ratios and utility, in ascending order of user-equipment identifier

#### Scenario: Centralized reward
- **WHEN** a step completes under the centralized handler
- **THEN** the reward is the mean scaled utility of the active user equipments, and the handler asserts that every scaled utility lies in `[-1, 1]`

#### Scenario: Wrong number of actions
- **WHEN** the centralized handler receives an action whose length does not equal the number of user equipments
- **THEN** the call fails with an explicit error

#### Scenario: Centralized control requires a static population
- **WHEN** an episode is reset with the centralized handler and an arrival model under which user equipments arrive late or depart early
- **THEN** the reset fails, because a fixed-size action and observation vector cannot represent a changing population

### Requirement: Multi-agent control
The multi-agent handler SHALL present each user equipment as its own agent with its own observation and reward, and SHALL include only currently active user equipments.

#### Scenario: Multi-agent spaces
- **WHEN** the multi-agent handler is used
- **THEN** the action space and observation space are dictionaries keyed by user-equipment identifier, each holding that agent's discrete action space and its own bounded observation vector

#### Scenario: Multi-agent observation
- **WHEN** the multi-agent handler produces observations
- **THEN** it returns one flat vector per currently active user equipment, concatenating its connections, normalized signal-to-noise ratios, own utility, the broadcast utilities of base stations in range and the broadcast connection counts of base stations in range

#### Scenario: Only active agents appear
- **WHEN** a user equipment is not active, or the episode's time is up
- **THEN** no observation is returned for it

#### Scenario: Multi-agent reward encourages coordination
- **WHEN** a step completes under the multi-agent handler
- **THEN** each active user equipment's reward combines its own scaled utility with the utilities of the base stations in its range, averaged over the number of user equipments those base stations serve, so that an agent that overloads a nearby cell is penalized

### Requirement: Handler-supplied step information
A handler SHALL be able to contribute entries to the info dictionary, and SHALL contribute none by default.

#### Scenario: Default handler info
- **WHEN** a handler does not override the info hook
- **THEN** it contributes no entries and the info dictionary contains only the tracked metrics
