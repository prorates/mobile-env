from typing import ClassVar

import numpy as np
from gymnasium import spaces

from mobile_env.handlers.handler import Handler


class MComCentralHandler(Handler):
    features: ClassVar[list[str]] = ["connections", "snrs", "utility"]

    @classmethod
    def ue_obs_size(cls, env) -> int:
        return sum(env.feature_sizes[ftr] for ftr in cls.features)

    @classmethod
    def action_space(cls, env) -> spaces.MultiDiscrete:
        # define multi-discrete action space for central setting
        # each element of a multi-discrete action denotes one UE's decision
        return spaces.MultiDiscrete([env.NUM_STATIONS + 1 for _ in env.users])

    @classmethod
    def observation_space(cls, env) -> spaces.Box:
        # observation is a single vector of concatenated UE representations
        size = cls.ue_obs_size(env)
        return spaces.Box(low=-1.0, high=1.0, shape=(env.NUM_USERS * size,))

    @classmethod
    def action(cls, env, actions: tuple[int]) -> dict[int, int]:
        """Transform flattend actions to expected shape of core environment."""
        assert len(actions) == len(env.users), (
            "Number of actions must equal overall UEs."
        )

        users = sorted(env.users)
        return dict(zip(users, actions, strict=True))

    @classmethod
    def observation(cls, env) -> np.ndarray:
        """Select from & flatten observations from MA setting."""
        # select observations considered in the central setting
        obs = {
            ue_id: [obs_dict[key] for key in cls.features]
            for ue_id, obs_dict in env.features().items()
        }

        # flatten observation to single vector
        return np.concatenate([o for ue_obs in obs.values() for o in ue_obs])

    @classmethod
    def reward(cls, env):
        """The central agent receives the average UE utility as reward."""
        utilities = np.asarray(list(env.utilities.values()))
        # assert that rewards are in range [-1, +1]
        bounded = np.logical_and(utilities >= -1, utilities <= 1).all()
        assert bounded, "Utilities must be in range [-1, +1]"

        # return average utility of UEs to central agent as reward
        return np.mean(utilities)

    @classmethod
    def check(cls, env):
        # the episode ends at the time limit or once the last UE departed;
        # every UE must be present for all of it, else the fixed-size action
        # and observation vectors would not match the active population
        ep_end = min(env.EP_MAX_TIME, env.max_departure)
        assert all(
            ue.stime <= 0.0 and ue.extime >= ep_end for ue in env.users.values()
        ), "Central environment cannot handle a changing number of UEs."
