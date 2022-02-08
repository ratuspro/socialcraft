from calendar import weekday
from .cogntive_social_frame import CognitiveSocialFrame
from csf_manager import Context, Affordance


class Work(CognitiveSocialFrame):
    def __init__(self, working_days, workplace):
        super(Work, self).__init__()
        self._needed_perceptions = ["time_of_day", "weekday"]
        self.__workplace = workplace
        self.__working_days = working_days

    def is_salient(self, context: Context) -> bool:
        self.assert_valid_context(context)

        weekday = context.get_perception("weekday")
        if weekday not in self.__working_days:
            return False
            
        time = context.get_perception("time_of_day")
        if time > self.__sleep_time[0] and time < self.__sleep_time[1]:
            return True
        return False

    def get_affordances(self) -> list[Affordance]:
        affordances = []
        affordances.append(Affordance("WORK", self.__workplace, 1))
        return affordances
