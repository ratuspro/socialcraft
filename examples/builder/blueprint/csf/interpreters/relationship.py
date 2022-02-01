import csf.core

from .interpreter import Interpreter


class SocialRelationshipInterpreter(Interpreter):
    def __init__(self, friends: set[str] = {}, enemies: set[str] = {}) -> None:
        self.__friends = friends
        self.__enemies = enemies

    def process_perceptions(self, perceptions: csf.core.Context) -> set[csf.core.Perception]:
        social_labels = set()

        for perception in perceptions.get_perceptions(name="PLAYER"):
            if perception.name == "PLAYER" and perception.value in self.__friends:
                social_labels.add(csf.core.Perception("FRIEND", perception.value))
            elif perception.name == "PLAYER" and perception.value in self.__enemies:
                social_labels.add(csf.core.Perception("ENEMY", perception.value))
            else:
                social_labels.add(csf.core.Perception("STRANGER", perception.value))

        return social_labels
