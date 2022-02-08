from .interpreter import Interpreter
import csf.core


class WorkTimeInterpreter(Interpreter):
    def __init__(self) -> None:
        self.__workdays = {
            csf.core.Perception("WEEKDAY", 0),
            csf.core.Perception("WEEKDAY", 1),
            csf.core.Perception("WEEKDAY", 2),
            csf.core.Perception("WEEKDAY", 3),
            csf.core.Perception("WEEKDAY", 4),
        }

    def process_perceptions(self, perceptions: csf.core.Context) -> set[csf.core.Perception]:
        if not self.__workdays.isdisjoint(perceptions.get_perceptions("WEEKDAY")):

            time = list(perceptions.get_perceptions("TIME"))[0].value

            if 1500 < time < 12000:
                return {csf.core.Perception("WORKTIME", 1)}

        return {csf.core.Perception("WORKTIME", 0)}

    def __str__(self) -> str:
        return f"<WorkTimeInterpreter>"


class SleepInterpreter(Interpreter):
    def __init__(self, min_hour: int, max_hour: int) -> None:
        self.__sleep_interval = (min_hour, max_hour)

    def process_perceptions(self, perceptions: csf.core.Context) -> set[csf.core.Perception]:
        time = list(perceptions.get_perceptions("TIME"))[0].value

        if self.__sleep_interval[0] < time < self.__sleep_interval[1]:
            return {csf.core.Perception("SLEEPTIME", 1)}

        return {csf.core.Perception("SLEEPTIME", 0)}

    def __str__(self) -> str:
        return f"<SleepInterpreter>"


class PartyTimeInterpreter(Interpreter):
    def __init__(self) -> None:
        self.__workdays = {
            csf.core.Perception("WEEKDAY", 0),
            csf.core.Perception("WEEKDAY", 1),
            csf.core.Perception("WEEKDAY", 2),
            csf.core.Perception("WEEKDAY", 3),
            csf.core.Perception("WEEKDAY", 4),
        }
        self.__offdays = {
            csf.core.Perception("WEEKDAY", 5),
            csf.core.Perception("WEEKDAY", 6),
        }

    def process_perceptions(self, perceptions: csf.core.Context) -> set[csf.core.Perception]:

        if not self.__workdays.isdisjoint(perceptions.get_perceptions("WEEKDAY")):
            time = list(perceptions.get_perceptions("TIME"))[0].value

            if 12100 < time < 19500:
                return {csf.core.Perception("PARTYTIME", 1)}

        elif not self.__offdays.isdisjoint(perceptions.get_perceptions("WEEKDAY")):
            time = list(perceptions.get_perceptions("TIME"))[0].value

            if 400 < time < 14000:
                return {csf.core.Perception("PARTYTIME", 1)}

        return {csf.core.Perception("PARTYTIME", 0)}

    def __str__(self) -> str:
        return f"<PartyTimeInterpreter>"


class InAreaInterpreter(Interpreter):
    def __init__(self, area_center, area_radius, label_feature) -> None:
        self.__area_center = area_center
        self.__area_radius = area_radius
        self.__label_feature = label_feature

    def process_perceptions(self, perceptions: csf.core.Context) -> set[csf.core.Perception]:
        player_position = list(perceptions.get_perceptions("SELF_POSITION"))[0].value

        if player_position.distanceTo(self.__area_center) < self.__area_radius:
            return {csf.core.Perception(self.__label_feature, 1)}

        return set()

    def __str__(self) -> str:
        return f"<InAreaInterpreter>"


class BlockInAreaInterpreter(Interpreter):
    def __init__(self, area_center, area_radius, block_to_identify, label_to_add_feature) -> None:
        self.__area_center = area_center
        self.__area_radius = area_radius
        self.__block_to_identify = block_to_identify
        self.__label_to_add_feature = label_to_add_feature

    def process_perceptions(self, perceptions: csf.core.Context) -> set[csf.core.Perception]:

        player_position = list(perceptions.get_perceptions("PLAYER_POSITION"))[0].value

        if player_position.distanceTo(self.__area_center) < self.__area_radius:
            return {csf.core.Perception(self.__label_to_add_feature, 1)}

        return set()

    def __str__(self) -> str:
        return f"<InAreaInterpreter>"
