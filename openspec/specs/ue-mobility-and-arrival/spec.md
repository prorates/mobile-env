## Purpose

Defines where user equipments are and when they are present: the mobility model that places and moves them across the area, and the arrival model that decides when each one starts requesting service and when it departs.

## Requirements

### Requirement: Mobility model interface
A mobility model SHALL provide a user equipment's initial position for an episode and its position after one time step, and SHALL be replaceable by a custom implementation.

#### Scenario: Custom mobility model
- **WHEN** a caller configures a custom mobility model
- **THEN** the environment uses it for every initial placement and every per-step movement

#### Scenario: Positions stay inside the area
- **WHEN** initial positions are drawn for an episode
- **THEN** every user equipment is placed within the configured area bounds

### Requirement: Default random-waypoint movement
The default mobility model SHALL move each user equipment in a straight line towards a randomly drawn waypoint at its own velocity, and SHALL draw a new waypoint once the current one is reached.

#### Scenario: Moving towards a waypoint
- **WHEN** a user equipment is further from its waypoint than one step of its velocity
- **THEN** it advances by exactly its velocity along the straight line towards that waypoint

#### Scenario: Reaching a waypoint
- **WHEN** a user equipment is within one step of its velocity of its waypoint
- **THEN** it is placed exactly on the waypoint and a new waypoint is drawn for the following step

### Requirement: Arrival model interface
An arrival model SHALL provide each user equipment's arrival time and departure time for an episode, and SHALL be replaceable by a custom implementation.

#### Scenario: Times are drawn at reset
- **WHEN** an episode is reset
- **THEN** every user equipment receives an arrival time and a departure time from the arrival model before the first step

### Requirement: Default no-departure arrival
The default arrival model SHALL have every user equipment request service from the start of the episode and remain present until the episode time limit, so the population never changes.

#### Scenario: Static population
- **WHEN** the default arrival model is used
- **THEN** every user equipment is active from the first step and none departs before the episode's time limit

### Requirement: Reproducible and optionally continuing random streams
Stochastic mobility and arrival models SHALL draw from a seeded random stream, and SHALL either restart that stream at every episode or continue it across episodes according to the per-episode reseeding flag.

#### Scenario: Reseeding each episode
- **WHEN** per-episode reseeding is enabled
- **THEN** every episode draws the same initial positions, waypoints, arrival times and departure times

#### Scenario: Continuing across episodes
- **WHEN** per-episode reseeding is disabled
- **THEN** successive episodes continue the same random stream and therefore differ from one another, while the whole run remains reproducible from the configured seed
