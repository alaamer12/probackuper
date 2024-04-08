from abc import abstractmethod, ABC

class ICommand(ABC):
    @abstractmethod
    def execute(self):
        pass