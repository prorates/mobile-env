# RLlib Integration

## Summary

Ray RLlib expects a different multi-agent shape than the environment's own, and this wrapper is the adapter between them. It re-declares the spaces per agent rather than per environment, and translates the environment's single truncation flag into the per-agent termination and truncation dictionaries RLlib requires — keyed by the agents present in the *previous* observation, since an agent that has just departed must still be reported as finished. Because RLlib bootstraps a value function from the last step an agent acted in, the wrapper also synthesises a final observation and reward for any agent that acted and was truncated in the same step. Termination is always false for every agent, because the environment has no terminal state; only truncation ever fires. The environment's info is placed under RLlib's shared-info key so that info keys never fall outside the set of returned observations.

## Purpose

Defines the adapter that lets the multi-agent environment be trained with Ray RLlib, which expects a per-agent view of spaces and per-agent termination dictionaries rather than the environment's own multi-agent form.

## Requirements

### Requirement: RLlib multi-agent adapter
A wrapper SHALL present a multi-agent environment as an RLlib multi-agent environment, exposing the set of agents that may ever appear, the set currently acting, the maximum episode length, and the action and observation space of every agent keyed by agent identifier.

#### Scenario: Wrapping an environment
- **WHEN** a multi-agent environment is wrapped
- **THEN** the wrapper reports one possible agent per user equipment, the environment's episode time limit as the maximum number of steps, and per-agent space mappings keyed by agent identifier — a discrete action over the no-operation and the base stations, and a bounded observation vector of the handler's feature size

#### Scenario: Wrapping an already-wrapped environment
- **WHEN** the environment passed in is enclosed in gymnasium wrappers rather than being the environment itself
- **THEN** the wrapper unwraps it to reach the underlying environment, and rejects anything that is not one

#### Scenario: The acting set follows the episode
- **WHEN** a step or reset changes which user equipments are active
- **THEN** the set of currently acting agents is updated to match, while the set of possible agents stays fixed for the lifetime of the environment

### Requirement: Per-agent episode signals
The wrapper SHALL report termination and truncation per agent as well as for the episode as a whole, keyed by the agents that were present in the previous observation.

#### Scenario: An agent leaves
- **WHEN** a user equipment that was present in the previous step is no longer active after a step
- **THEN** it is reported as truncated for that step, while agents still active are not

#### Scenario: Episode end
- **WHEN** the underlying episode's time limit is reached
- **THEN** the wrapper reports truncation for the episode as a whole, and every agent that was active going into that step is reported truncated, since no further step remains for it to act in

### Requirement: Final observation and reward for truncated agents
The wrapper SHALL provide an observation and a reward for every agent that acted in a step and is reported as truncated in that same step, so that RLlib can bootstrap a value estimate from it.

#### Scenario: An acting agent is truncated
- **WHEN** an agent submitted an action in a step and the environment reports no observation for it, because it departed or the episode ended
- **THEN** the wrapper supplies a zero observation matching that agent's observation space and a reward of zero, leaving any reward the environment did report untouched

#### Scenario: No natural termination
- **WHEN** any step completes
- **THEN** termination is reported as false for every agent and for the episode as a whole, because the environment has no terminal state

### Requirement: Info keys compatible with RLlib
The wrapper SHALL place the environment's info under RLlib's shared-info key, so that info keys never fall outside the set of returned observations.

#### Scenario: Info is namespaced
- **WHEN** a step returns
- **THEN** the environment's entire info dictionary appears under RLlib's common-info key rather than being keyed by agent

### Requirement: Rendering passes through
The wrapper SHALL delegate rendering to the wrapped environment.

#### Scenario: Rendering a wrapped environment
- **WHEN** the wrapper is rendered
- **THEN** the wrapped environment's frame is produced unchanged
