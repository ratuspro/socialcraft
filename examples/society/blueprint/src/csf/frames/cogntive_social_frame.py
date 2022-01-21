from abc import abstractclassmethod, ABC


class CognitiveSocialFrame(ABC):
    def __init__(self) -> None:
        self._needed_labels = []

    @abstractclassmethod
    def is_salient(self) -> bool:
        pass

    @abstractclassmethod
    def get_affordances(self):
        pass

    def assert_valid_context(self, context) -> None:
        for neeeded_perception in self._needed_perceptions:
            if context.get_perception(neeeded_perception) is None:
                raise Exception(
                    f"Expected perception with label '{neeeded_perception}'"
                )
