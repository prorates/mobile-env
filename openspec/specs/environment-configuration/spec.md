## Purpose

Defines how an environment is configured and extended: the default parameter set, how a caller's partial configuration is merged into it, and how the simulation models (channel, movement, arrival, scheduler, utility, control handler) are replaced with custom implementations.

## Requirements

### Requirement: Published default configuration
The environment SHALL publish its complete default configuration so a caller can inspect it, copy it and modify individual entries without knowing the internal defaults.

#### Scenario: Reading the defaults
- **WHEN** the environment class is asked for its default configuration
- **THEN** it returns a dictionary containing the map size, episode time limit, seed and per-episode reseeding flag; the model classes used for arrival, channel, scheduler, movement, utility and control handling; the base-station and user-equipment parameter sets; one parameter dictionary per model; and the tracked-metric registry

#### Scenario: Defaults describe a runnable environment
- **WHEN** an environment is constructed with no configuration at all
- **THEN** it is fully operational, using a 200×200 area, a 100-step episode limit, seed `0`, no per-episode reseeding, and the built-in Okumura–Hata channel, random-waypoint movement, no-departure arrival, resource-fair scheduler, bounded-log utility and centralized control handler

### Requirement: Partial configuration is merged, not replaced
A caller SHALL be able to supply a partial configuration; every key it does not mention SHALL keep its default value, including keys nested inside a sub-dictionary.

#### Scenario: Overriding one nested parameter
- **WHEN** an environment is constructed with a configuration that sets only one base-station parameter
- **THEN** that parameter takes the supplied value and every other base-station and top-level parameter keeps its default

### Requirement: Pluggable simulation models
Each simulation model SHALL be selectable by assigning a class to its configuration key, and its constructor arguments SHALL be supplied through the matching parameter dictionary.

#### Scenario: Replacing the channel model
- **WHEN** a caller assigns a custom channel class to the channel configuration key and puts that class's constructor arguments in the channel parameter dictionary
- **THEN** the environment instantiates the custom class with those arguments and uses it for every path-loss, signal-to-noise-ratio and data-rate computation

#### Scenario: Replacing the control handler
- **WHEN** a caller assigns a different control handler to the handler configuration key
- **THEN** the environment's action space, observation space, action interpretation, observations and rewards are all defined by that handler

### Requirement: Derived per-model seeds
The environment SHALL derive a distinct, reproducible seed for each stochastic model from the single configured seed, so that models do not share a random stream.

#### Scenario: Seeds are distributed to models
- **WHEN** an environment is configured with a seed
- **THEN** the arrival, channel, scheduler, movement and utility parameter dictionaries each receive their own seed derived deterministically from it, and re-running with the same configured seed yields the same per-model seeds
