from typing import Any, Optional
from vector3 import Vector3


class Player:

    __name: str
    __position: Vector3

    def __init__(self, name: str, position: Vector3) -> None:
        self.__name = name
        self.__position = position

    @property
    def name(self) -> str:
        return self.__name

    @property
    def position(self) -> Vector3:
        return self.__position

    def __str__(self) -> str:
        return f"Player {self.__name} at {self.__position}"


class Block:
    __type: str
    __position: Vector3

    def __init__(self, type: str, position: Vector3) -> None:
        self.__type = type
        self.__position = position

    @property
    def type(self) -> str:
        return self.__type

    @property
    def position(self) -> Vector3:
        return self.__position

    def __str__(self) -> str:
        return f"{self.__type} at {self.__position}"


class Perception:

    __label: str
    __salience: float
    __target: Optional[Any]

    def __init__(self, label: str, salience: float, target: Optional[Any]) -> None:
        self.__label = label
        self.__salience = salience
        self.__target = target

    @property
    def label(self) -> str:
        return self.__label

    @property
    def salience(self) -> float:
        return self.__salience

    @property
    def target(self) -> Optional[Any]:
        return self.__target

    def __str__(self) -> str:
        return "{:<30}[{:>3}] => {}".format(self.label, self.salience, self.target)
