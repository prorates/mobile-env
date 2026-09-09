## Purpose

Defines how a user equipment's data rate is turned into a quality-of-experience utility, and how that utility is scaled into the bounded range used for rewards and observations — the piece that makes quality of experience grow sub-linearly with data rate.

## Requirements

### Requirement: Utility model interface
A utility model SHALL map a data rate to a utility value, and SHALL provide a scaling and an inverse scaling between that value and the bounded range used for rewards and observations.

#### Scenario: Custom utility model
- **WHEN** a caller configures a custom utility model
- **THEN** the environment uses it for every reward, every utility observation and every utility metric

#### Scenario: Scaling round-trips
- **WHEN** a utility value is scaled and then unscaled
- **THEN** the original value is recovered

### Requirement: Bounded scaled range
Scaled utilities SHALL lie in the range `[-1, 1]`, with the model's lower utility bound mapping to `-1` and its upper bound to `1`.

#### Scenario: Bounds map to the range endpoints
- **WHEN** the lower and upper utility bounds are scaled
- **THEN** they yield `-1` and `1` respectively, and every intermediate utility yields a value between them

### Requirement: Default bounded logarithmic utility
The default utility model SHALL be logarithmic in the data rate and SHALL be clipped to a configurable lower and upper bound, so that quality of experience saturates rather than growing without limit.

#### Scenario: Diminishing returns
- **WHEN** a user equipment's data rate increases
- **THEN** its utility increases logarithmically and stops increasing once the upper bound is reached

#### Scenario: No service
- **WHEN** a user equipment's data rate is zero or negative
- **THEN** its utility is the configured lower bound
