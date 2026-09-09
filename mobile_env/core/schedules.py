from abc import abstractmethod
from typing import List

from mobile_env.core.entities import BaseStation


class Scheduler:
    def __init__(self, **kwargs):
        pass

    def reset(self) -> None:
        pass

    @abstractmethod
    def share(self, bs: BaseStation, rates: List[float]) -> List[float]:
        pass


class ResourceFair(Scheduler):
    def share(self, bs: BaseStation, rates: List[float]) -> List[float]:
        return [rate / len(rates) for rate in rates]


class RateFair(Scheduler):
    def share(self, bs: BaseStation, rates: List[float]) -> List[float]:
        # equalize the granted rate: f_i * rates[i] = R for all i with sum(f_i) = 1
        # yields R = 1 / sum(1 / rates[i]). One entry per connection, as the
        # caller zips the result against the base station's connections.
        if not rates:
            return []

        # a connection out of range contributes a zero max. rate; the equal-rate
        # limit as any rate approaches zero is zero, so grant nothing to anyone
        if any(rate <= 0.0 for rate in rates):
            return [0.0 for _ in rates]

        total_inv_rate = sum([1 / rate for rate in rates])
        return [1 / total_inv_rate for _ in rates]
