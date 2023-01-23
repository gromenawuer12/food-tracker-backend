from abc import ABC, abstractmethod

class RootMethodResolve(ABC):
    @abstractmethod
    def resolve(self, paths, event) -> None:
        pass