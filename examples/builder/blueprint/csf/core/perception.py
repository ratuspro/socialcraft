from typing import Any


class Perception:
    def __init__(self, name: str, value: Any) -> None:
        self.__name = name
        self.__value = value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> Any:
        return self.__value

    def __hash__(self) -> int:
        return hash(self.name) + hash(self.value)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Perception):
            return False
        return self.__name == o.name and self.__value == o.value

    def __str__(self) -> str:
        return f"<name: {self.name}, value: {str(self.value)}>"
