from .cogntive_social_frame import CognitiveSocialFrame
from csf_manager import Context, Affordance


class Sleep(CognitiveSocialFrame):
    def __init__(self, sleeping_time: tuple[int, int]):
        super(Sleep, self).__init__()
        self._needed_perceptions = ["time_of_day"]
        self.__sleep_time = sleeping_time

    def is_salient(self, context: Context) -> bool:
        self.assert_valid_context(context)

        time = context.get_perception("time_of_day")
        if time > self.__sleep_time[0] and time < self.__sleep_time[1]:
            return True
        return False

    def get_affordances(self) -> list[Affordance]:
        affordances = []
        affordances.append(Affordance("CAN_SLEEP", None, 1))
        return affordances
