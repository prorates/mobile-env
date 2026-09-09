## Purpose

Defines the radio channel contract: how a channel model turns the geometry and radio parameters of a base station and a user equipment into a power loss, a signal-to-noise ratio and an achievable data rate, and the default Okumura–Hata model shipped with the environment.

## Requirements

### Requirement: Channel model interface
A channel model SHALL provide the power loss between a base station and a user equipment, SHALL be resettable between episodes, and SHALL be replaceable by a custom implementation that only has to supply the power loss.

#### Scenario: Custom channel supplies only power loss
- **WHEN** a caller provides a channel model that implements power loss and configures the environment to use it
- **THEN** the environment derives signal-to-noise ratios, data rates and coverage isolines from that power loss without further code

#### Scenario: Reset between episodes
- **WHEN** an episode is reset
- **THEN** the channel model's `reset` is invoked before the new episode begins

### Requirement: Signal-to-noise ratio
The signal-to-noise ratio SHALL be derived from the base station's transmit power reduced by the model's power loss, relative to the user equipment's noise level.

#### Scenario: Ratio falls with distance
- **WHEN** a user equipment moves further from a base station under a model whose power loss grows with distance
- **THEN** the reported signal-to-noise ratio decreases

### Requirement: Achievable data rate
The maximum data rate of a connection SHALL follow the Shannon relation over the base station's bandwidth, and SHALL be zero when the signal-to-noise ratio does not exceed the user equipment's threshold.

#### Scenario: Rate above the threshold
- **WHEN** the signal-to-noise ratio exceeds the user equipment's threshold
- **THEN** the maximum data rate is the base station's bandwidth multiplied by the base-two logarithm of one plus the signal-to-noise ratio

#### Scenario: Rate below the threshold
- **WHEN** the signal-to-noise ratio does not exceed the user equipment's threshold
- **THEN** the maximum data rate is zero

### Requirement: Coverage isolines
The channel model SHALL be able to report, for a given base station and a given data-rate threshold, the boundary within the map at which a nominal user equipment can still achieve that rate.

#### Scenario: Isoline for a data-rate threshold
- **WHEN** an isoline is requested for a base station, a nominal user-equipment configuration, the map bounds and a data-rate threshold
- **THEN** the model returns a closed set of points around the base station, clipped to the map, at which the achievable data rate is the requested threshold

### Requirement: Default Okumura–Hata model
The default channel model SHALL be the Okumura–Hata path-loss model, parameterized by carrier frequency, base-station height, user-equipment height and their separation.

#### Scenario: Zero separation is well defined
- **WHEN** a user equipment is at the exact position of a base station
- **THEN** the model returns a finite power loss instead of failing on the logarithm of zero
