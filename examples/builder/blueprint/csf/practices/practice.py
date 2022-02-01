from abc import abstractmethod, ABC


class Practice(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass
