## ADDED Requirements

### Requirement: Declared render frame rate
The environment SHALL declare the frame rate its rendering is intended to be played back at, alongside its supported render modes.

#### Scenario: Frame rate is advertised
- **WHEN** a consumer reads the environment's render metadata
- **THEN** it finds a declared frame rate in addition to the list of render modes, and no warning is emitted about an undeclared rate

#### Scenario: Recording at the declared rate
- **WHEN** frames collected in image-array mode are assembled into a video at the declared frame rate
- **THEN** playback advances one simulation step per frame at that rate
