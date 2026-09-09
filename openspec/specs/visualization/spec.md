# Visualization

## Summary

Rendering produces a single frame combining a live picture of the network with a dashboard of how the episode is going. The network view is not decoration: user equipments are coloured by quality of experience, each connection is coloured by its share of that user equipment's total, and every base station is drawn with both its connectivity boundary and the boundary within which 1 MB/s is still achievable — so an overloaded cell or a user equipment stranded between cells is visible at a glance. The same frame is available either as an on-screen window or as an image array for recording video. Rendering before the first step yields an empty frame rather than an error, and rendering after close does nothing at all.

## Purpose

Defines what the environment shows when it is rendered: a live picture of the network — users, base stations, their coverage and their connections, coloured by quality of experience — alongside a dashboard of how the episode is progressing.

## Requirements

### Requirement: Rendering modes
The environment SHALL support rendering as an on-screen window and as an image array, SHALL declare both modes, and SHALL reject any other mode.

#### Scenario: Image output
- **WHEN** the environment is created in image-array mode and rendered
- **THEN** it returns the current frame as a height-by-width-by-three array of 8-bit colour values, suitable for recording a video

#### Scenario: Window output
- **WHEN** the environment is created in window mode and rendered
- **THEN** the frame is drawn in an on-screen window, and closing that window closes the environment

#### Scenario: Unsupported mode
- **WHEN** an environment is constructed with a render mode that is not declared
- **THEN** construction fails with an explicit error

### Requirement: Network view
The rendered frame SHALL show the simulated area with every base station, every active user equipment and every established connection.

#### Scenario: Users are coloured by quality of experience
- **WHEN** the network view is drawn
- **THEN** each active user equipment is drawn at its position, labelled by its identifier and coloured on a scale from its lower to its upper utility bound

#### Scenario: Connections are coloured by contribution
- **WHEN** a user equipment holds several connections
- **THEN** each connection is drawn as a line to its base station, coloured by that connection's share of the user equipment's total quality of experience

#### Scenario: Coverage is shown
- **WHEN** the network view is drawn
- **THEN** each base station is drawn with its identifier, its connectivity boundary, and the boundary within which a user equipment could still receive 1 MB/s

### Requirement: Episode dashboard
The rendered frame SHALL show, next to the network view, the current and episode-average mean data rate and mean utility, and the history of mean utility and of the number of connected user equipments over the episode.

#### Scenario: Dashboard values
- **WHEN** the dashboard is drawn after at least one step
- **THEN** it shows the latest and the episode-average mean data rate and mean utility, and two time series over the episode's time axis

#### Scenario: Rendering before the first step
- **WHEN** `render()` is called before any step has been taken
- **THEN** the frame is produced with the panels empty rather than failing

### Requirement: Rendering stops after close
Once the environment has been closed, rendering SHALL be a no-op.

#### Scenario: Render after close
- **WHEN** `render()` is called after `close()`
- **THEN** nothing is drawn and no error is raised
