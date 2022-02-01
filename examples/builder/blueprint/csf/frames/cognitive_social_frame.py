from abc import abstractclassmethod, ABC

import csf.core


class CognitiveSocialFrame(ABC):
    def __init__(self, perception_labels: set[str]) -> None:
        self._needed_labels = perception_labels

    @abstractclassmethod
    def is_salient(self, context: csf.core.Context) -> bool:
        pass

    @abstractclassmethod
    def get_affordances(self) -> set:
        pass

    def assert_valid_context(self, context) -> None:
        for neeeded_perception in self._needed_labels:
            if context.get_perceptions(neeeded_perception) is None:
                raise Exception(f"Expected perception with label '{neeeded_perception}'")
