import abc

from gymnasium.spaces.space import Space


class Handler:
    """Defines Gymnasium interface methods called by core simulation."""

    @classmethod
    @abc.abstractmethod
    def action_space(cls, env) -> Space:
        """Defines action space for passed environment."""

    @classmethod
    @abc.abstractmethod
    def observation_space(cls, env) -> Space:
        """Defines observation space for passed environment."""

    @classmethod
    @abc.abstractmethod
    def action(cls, env, action) -> dict[int, int]:
        """Transform passed action(s) to dict shape expected by simulation."""

    @classmethod
    @abc.abstractmethod
    def observation(cls, env):
        """Computes observations for agent."""

    @classmethod
    @abc.abstractmethod
    def reward(cls, env):
        """Computes rewards for agent."""

    @classmethod
    def check(cls, env):
        """Check if handler is applicable to simulation configuration."""

    @classmethod
    def info(cls, env):
        """Compute information for feedback loop."""
        return {}
