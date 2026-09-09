## Purpose

Defines how a base station divides its limited radio resources among the user equipments connected to it, which is what makes connections compete and turns multi-cell selection into a coordination problem.

## Requirements

### Requirement: Scheduler interface
A scheduler SHALL take a base station and the maximum data rate each connected user equipment could achieve if it received all of that base station's resources, and SHALL return the data rate actually granted to each of those connections.

#### Scenario: One rate per connection
- **WHEN** a base station with connected user equipments schedules its resources
- **THEN** the scheduler returns one granted data rate per connected user equipment, in the same order as the maximum rates it was given

#### Scenario: Custom scheduler
- **WHEN** a caller configures a custom scheduler
- **THEN** the environment uses it for every base station's resource allocation

### Requirement: Default resource-fair scheduling
The default scheduler SHALL divide each base station's resources equally among its connections, so each connection receives its maximum achievable rate divided by the number of connections.

#### Scenario: Equal split
- **WHEN** several user equipments are connected to one base station under the default scheduler
- **THEN** each receives its own maximum achievable rate divided by the number of connected user equipments, so a user equipment with a better channel still gets a higher rate than one with a worse channel

#### Scenario: Sole connection
- **WHEN** exactly one user equipment is connected to a base station
- **THEN** it receives its full maximum achievable data rate

### Requirement: Rate-fair scheduling
A rate-fair scheduler SHALL be available as an alternative that equalizes the data rate across a base station's connections rather than the share of resources.

#### Scenario: Equal rates
- **WHEN** several user equipments with different maximum achievable rates are connected to one base station under the rate-fair scheduler
- **THEN** every connection receives the same data rate, set by the harmonic relation of their maximum achievable rates
