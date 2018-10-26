from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def update(self, *args):
        raise NotImplementedError
