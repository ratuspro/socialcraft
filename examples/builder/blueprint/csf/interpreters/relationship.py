import csf.core

from .interpreter import Interpreter


class SocialRelationshipInterpreter(Interpreter):
    def __init__(self, friends: set[str] = None, enemies: set[str] = None) -> None:
        self.__friends = {} if friends is None else friends
        self.__enemies = {} if enemies is None else enemies

    def process_perceptions(self, perceptions: csf.core.Context) -> set[csf.core.Perception]:
        social_labels = set()

        for perception in perceptions.get_perceptions("PLAYER"):
            if perception.name == "PLAYER" and perception.value in self.__friends:
                social_labels.add(csf.core.Perception("FRIEND", perception.value))
            elif perception.name == "PLAYER" and str(perception.value) in self.__enemies:
                social_labels.add(csf.core.Perception("ENEMY", perception.value))
            else:
                social_labels.add(csf.core.Perception("STRANGER", perception.value))

        return social_labels
