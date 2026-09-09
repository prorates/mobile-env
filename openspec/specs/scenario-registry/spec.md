# Scenario Registry

## Summary

The package ships three fixed network topologies — small, medium and large — so that results published against `mobile-env` are comparable between users rather than depending on a topology each experimenter invented. Each fixes the area, the base-station positions and the user-equipment count, while still accepting the same configuration dictionary as the base environment, so a custom channel model can be studied on a standard topology. Importing the package registers all six combinations of the three sizes and the two control modes with Gymnasium, so no explicit registration call is ever needed. The identifiers follow one stable pattern, `mobile-<size>-<mode>-v0`.

## Purpose

Defines the ready-made environments the package ships and how they are obtained: three network sizes crossed with the two control modes, registered with Gymnasium so an experimenter can create any of them by identifier with no setup.

## Requirements

### Requirement: Predefined scenarios
The package SHALL ship a small, a medium and a large scenario, each with a fixed area, a fixed set of base-station positions and a fixed number of user equipments, so results are comparable across users of the package.

#### Scenario: Small scenario
- **WHEN** the small scenario is created
- **THEN** it has a 200×200 area, three base stations at fixed positions and five user equipments

#### Scenario: Medium scenario
- **WHEN** the medium scenario is created
- **THEN** it has a 200×300 area, seven base stations at fixed positions and fifteen user equipments

#### Scenario: Large scenario
- **WHEN** the large scenario is created
- **THEN** it has a 300×300 area, thirteen base stations at fixed positions and thirty user equipments

### Requirement: Scenarios accept configuration
Each predefined scenario SHALL accept the same partial configuration and render mode as the base environment, overriding its defaults while keeping its fixed topology.

#### Scenario: Customizing a predefined scenario
- **WHEN** a predefined scenario is created with a configuration that replaces a simulation model
- **THEN** the scenario keeps its base-station positions and user-equipment count and uses the supplied model

### Requirement: Gymnasium registration
Importing the package SHALL register every combination of scenario and control mode with Gymnasium under a stable identifier, so no explicit registration call is needed.

#### Scenario: Creating a registered environment
- **WHEN** the package is imported and an environment is created by the identifier `mobile-<size>-<mode>-v0`, where size is `small`, `medium` or `large` and mode is `central` or `ma`
- **THEN** the corresponding scenario is created with the matching control handler already configured

#### Scenario: All combinations exist
- **WHEN** the registered identifiers are listed
- **THEN** all six combinations of the three sizes and the two control modes are present
