## Purpose

Defines the simulated mobile network itself: base stations and user equipments, when a downlink connection may exist between them, how base-station resources become per-connection data rates, and how those data rates become the quality-of-experience utilities that drive rewards and metrics.

## Requirements

### Requirement: Network entities
The simulation SHALL model base stations and user equipments as entities with stable identifiers and radio parameters.

#### Scenario: Base station properties
- **WHEN** a base station is created
- **THEN** it has a unique identifier, a fixed position in the area, a bandwidth, a carrier frequency, a transmit power and an antenna height

#### Scenario: User equipment properties
- **WHEN** a user equipment is created
- **THEN** it has a unique identifier, a movement velocity, a signal-to-noise-ratio threshold below which it cannot hold a connection, a noise level, an antenna height, and — once an episode starts — a position, an arrival time and a departure time

### Requirement: Connectivity condition
A downlink connection between a base station and a user equipment SHALL be possible only while the signal-to-noise ratio between them exceeds that user equipment's threshold.

#### Scenario: Reachable base stations
- **WHEN** the set of base stations a user equipment could connect to is requested
- **THEN** it contains exactly those base stations whose signal-to-noise ratio at the user equipment's current position exceeds its threshold

### Requirement: Connection changes are toggles
An action naming a base station SHALL toggle that user equipment's connection to it: connect if currently disconnected and in range, disconnect if currently connected.

#### Scenario: Establishing a connection
- **WHEN** an active user equipment selects a base station it is not connected to and that base station is in range
- **THEN** the connection is established, in addition to any connections the user equipment already holds

#### Scenario: Releasing a connection
- **WHEN** an active user equipment selects a base station it is already connected to
- **THEN** that connection is released

#### Scenario: Out-of-range selection has no effect
- **WHEN** an active user equipment selects a base station that is not in range and it is not connected to it
- **THEN** no connection is established

#### Scenario: No-operation action
- **WHEN** the no-operation action is selected, or the action belongs to a user equipment that is not currently active
- **THEN** the set of connections is left unchanged

### Requirement: Connections are released when users move out of range
At each step, before actions are applied, the simulation SHALL release every connection whose signal-to-noise ratio has fallen to or below the user equipment's threshold.

#### Scenario: A moving user leaves a cell
- **WHEN** a connected user equipment has moved far enough that its signal-to-noise ratio to that base station no longer exceeds its threshold
- **THEN** the connection is released at the next step without any agent action

### Requirement: Base-station resources are shared among connections
Each base station SHALL compute the maximum data rate achievable for every connected user equipment and SHALL divide its resources among them according to the configured scheduler.

#### Scenario: Competing users share a cell
- **WHEN** several user equipments are connected to the same base station
- **THEN** each connection receives a share of that base station's resources determined by the scheduler, so adding another connection reduces the data rate of the existing ones

### Requirement: Aggregated user data rate
A user equipment's data rate SHALL be the sum of the data rates of all its connections.

#### Scenario: Multi-cell connection
- **WHEN** a user equipment is connected to more than one base station
- **THEN** its data rate is the sum of the rates of those connections, so additional connections can raise its total rate

### Requirement: Utilities in a bounded range
The simulation SHALL convert each active user equipment's aggregated data rate into a utility and SHALL scale that utility into the range `[-1, 1]` before it is used as a reward or observation.

#### Scenario: Utilities are computed for active users
- **WHEN** a step completes
- **THEN** every active user equipment has a utility derived from its aggregated data rate and scaled to `[-1, 1]`

### Requirement: Per-base-station utility
The simulation SHALL expose, for each base station, the average scaled utility of the user equipments connected to it.

#### Scenario: Busy base station
- **WHEN** a base station has at least one connected user equipment
- **THEN** its utility is the mean of the scaled utilities of those user equipments

#### Scenario: Idle base station
- **WHEN** a base station has no connected user equipment
- **THEN** its utility is the scaled lower utility bound

### Requirement: Active user population
A user equipment SHALL be active — that is, requesting service and eligible to act — only between its arrival time and its departure time, and the active set SHALL be ordered by identifier.

#### Scenario: A user arrives
- **WHEN** simulation time reaches a user equipment's arrival time
- **THEN** it joins the active set and its actions take effect

#### Scenario: A user departs
- **WHEN** simulation time reaches a user equipment's departure time
- **THEN** it leaves the active set and all of its connections are released
