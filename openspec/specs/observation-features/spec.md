# Observation Features

## Summary

The simulation computes one shared, named feature set per user equipment each step — connections, signal-to-noise ratios, own utility, broadcast base-station utilities and broadcast connection counts — from which each handler selects the subset it exposes. Keeping this vocabulary in one place is what lets the centralized handler use three features and the multi-agent handler five without either redefining what a feature means. Everything is normalized for direct use in a bounded observation space: connections are one-hot, signal-to-noise ratios are relative to the best base station the user equipment currently sees, and connection counts are relative to the total in range. The two broadcast features are limited to base stations actually in range, so an out-of-range base station reads as a defined placeholder rather than leaking information a real user equipment could not receive.

## Purpose

Defines the base set of per-user-equipment features the simulation computes each step, from which any control handler selects the observation it exposes — the shared, normalized vocabulary that keeps centralized, multi-agent and custom handlers consistent.

## Requirements

### Requirement: Base feature set
The simulation SHALL compute, for every user equipment each step, a named set of features: its current connections, its signal-to-noise ratios, its own utility, the broadcast utility of each base station, and the broadcast count of user equipments connected to each base station.

#### Scenario: Features are available for every user equipment
- **WHEN** the base feature set is requested
- **THEN** it contains an entry for every user equipment in the scenario, keyed by identifier, with all five named features present

#### Scenario: Feature sizes are published
- **WHEN** a handler asks for the size of a feature
- **THEN** the environment reports one element per base station for connections, signal-to-noise ratios, broadcast utilities and broadcast connection counts, and a single element for the user equipment's own utility

### Requirement: Consistent base-station ordering
Every per-base-station feature SHALL be ordered by base-station identifier, so that a given index refers to the same base station across all features and all steps.

#### Scenario: Index refers to one base station
- **WHEN** two per-base-station features are read at the same index
- **THEN** both refer to the same base station

### Requirement: Normalized feature values
All features SHALL be reported as normalized floating-point values suitable for direct use in a bounded observation space.

#### Scenario: Connections are one-hot
- **WHEN** a user equipment's connection feature is read
- **THEN** it is `1` at the position of each base station the user equipment is currently connected to and `0` elsewhere

#### Scenario: Signal-to-noise ratios are relative
- **WHEN** a user equipment's signal-to-noise-ratio feature is read
- **THEN** each value is that base station's ratio divided by the largest ratio the user equipment currently sees, so the best base station reads `1`

#### Scenario: Connection counts are relative
- **WHEN** a user equipment's broadcast connection-count feature is read
- **THEN** each value is that base station's number of connections divided by the total across the base stations in range

### Requirement: Broadcast features are limited to base stations in range
A user equipment SHALL only receive the broadcast utility and connection count of base stations it could connect to; for the others the feature SHALL carry a defined out-of-range value rather than leaking information.

#### Scenario: Out-of-range base station
- **WHEN** a base station is not in range of a user equipment
- **THEN** its broadcast utility for that user equipment is the scaled lower utility bound and its broadcast connection count is zero

### Requirement: Placeholder features for inactive users
A user equipment that is not currently active SHALL still have a well-defined feature entry, so that fixed-size observations remain valid.

#### Scenario: Inactive user equipment
- **WHEN** the base feature set is computed for a user equipment that has not yet arrived or has already departed
- **THEN** its connections and signal-to-noise ratios are all zero, its own utility and every broadcast utility are the scaled lower utility bound, and its broadcast connection counts are all one

#### Scenario: Utility before the first step
- **WHEN** a user equipment's utility has not been computed yet in this episode
- **THEN** its utility feature is the scaled lower utility bound
