from .perception import Perception


class Context:
    def __init__(self) -> None:
        self.__perceptions = set()

    def get_perceptions(self, name: str = None) -> list[Perception]:

        if name is None:
            return list(self.__perceptions)

        filtered_perceptions = set()
        for perception in self.__perceptions:
            if perception.name == name:
                filtered_perceptions.add(perception)

        return list(filtered_perceptions)

    def add_perception(self, perception: Perception) -> None:
        self.__perceptions.add(perception)

    def add_perceptions(self, perceptions: set[Perception]) -> None:
        for perception in perceptions:
            self.add_perception(perception)
