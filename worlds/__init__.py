
class World:
    def __init__(self, world=None):
        if world is not None:
            self.get_observation_shape = world.get_observation_shape
            self.get_action_shape = world.get_action_shape
            self.get_reward_shape = world.get_reward_shape

    def get_observation_shape(self): # -> shape [tuple of int] or None
        return None

    def get_action_shape(self): # -> shape [tuple of int]
        raise NotImplementedError("get_action_shape")

    def get_reward_shape(self): # -> shape [tuple of int]
        raise NotImplementedError("get_reward_shape")

    def start_episode(self, seed): # -> state
        raise NotImplementedError("start_episode")

    def __getattr__(self, name):
        if name in ("o_shape", "observation_shape"):
            return self.get_observation_shape()
        if name in ("a_shape", "action_shape"):
            return self.get_action_shape()
        if name in ("r_shape", "reward_shape"):
            return self.get_reward_shape()
        return object.__getattribute__(self, name)

class Episode:
    def get_observation(self): # -> observation [ndarray] or None
        return None

    def step(self, action): # -> reward [ndarray]
        raise NotImplementedError("step")

    def __next__(self):
        return self.get_observation()

    def __iter__(self):
        return self

from .Accuracy import Accuracy
from .BasicNet import BasicNet
from .Distribution import Distribution
from .Mnist import Mnist
from .Reinforce import Reinforce

def compose(World1, World2):
    return lambda *args, **kwargs: World1(World2(*args, **kwargs))

Reinforce = compose(Distribution, Reinforce)