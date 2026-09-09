from abc import abstractmethod

import numpy as np

from mobile_env.core.entities import UserEquipment


class Movement:
    def __init__(self, width: float, height: float, seed: int, reset_rng_episode: str, **kwargs):

        self.width, self.height = width, height
        self.reset_rng_episode = reset_rng_episode

        # RNG for movement and initial positions of UEs
        self.seed = seed
        self.rng: np.random.Generator | None = None

    def reset(self) -> None:
        """Reset state of movement object after episode ends."""
        # case: movement patterns remain unchanged between episodes
        if self.reset_rng_episode or self.rng is None:
            self.rng = np.random.default_rng(self.seed)

    @abstractmethod
    def move(self, ue: UserEquipment) -> tuple[float, float]:
        """Move UE at each time step."""

    @abstractmethod
    def initial_position(self, ue: UserEquipment) -> tuple[float, float]:
        """Reset position of UE e.g. after episode ends."""


class RandomWaypointMovement(Movement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # track waypoints and initial positions per UE
        self.waypoints: dict[UserEquipment, tuple[float, float]] = None
        self.initial: dict[UserEquipment, tuple[float, float]] = None

    def reset(self) -> None:
        super().reset()
        # NOTE: if RNG is not resetted after episode ends,
        # initial positions will differ between episodes
        self.waypoints = {}
        self.initial = {}

    def move(self, ue: UserEquipment) -> tuple[float, float]:
        """Move UE a step towards the random waypoint."""
        assert self.rng is not None, "reset() must run before move()"

        # generate random waypoint if UE has none so far
        if ue not in self.waypoints:
            wx = self.rng.uniform(0, self.width)
            wy = self.rng.uniform(0, self.height)
            self.waypoints[ue] = (wx, wy)

        position = np.array([ue.x, ue.y])
        waypoint = np.array(self.waypoints[ue])

        # if already close enough to waypoint, move directly onto waypoint
        if np.linalg.norm(position - waypoint) <= ue.velocity:
            # remove waypoint from dict after it has been reached
            return self.waypoints.pop(ue)

        # else move by self.velocity towards waypoint
        v = waypoint - position
        position = position + ue.velocity * v / np.linalg.norm(v)

        return tuple(position)

    def initial_position(self, ue: UserEquipment) -> tuple[float, float]:
        """Return initial position of UE at the beginning of the episode."""
        assert self.rng is not None, "reset() must run before initial_position()"

        if ue not in self.initial:
            x = self.rng.uniform(0, self.width)
            y = self.rng.uniform(0, self.height)
            self.initial[ue] = (x, y)

        x, y = self.initial[ue]
        return x, y
