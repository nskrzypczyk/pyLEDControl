from abc import ABC, abstractmethod


class AbstractEffect(ABC):
    @abstractmethod
    def build(self):
        """Prepares the necessary data which will be then passed to the respective controller to display the effect / mode"""
        pass
