import csf.core
import csf.practices
import json
from .cognitive_social_frame import CognitiveSocialFrame
from javascript import require

Vec3 = require("vec3")
pathfinder = require("mineflayer-pathfinder")


class LumberjackFrame(CognitiveSocialFrame):
    def __init__(self, bot, lumberyard_center, lumberyard_radius) -> None:
        super().__init__({"PARTYTIME"})
        self.__bot = bot
        self.__lumberyard_center = lumberyard_center
        self.__lumberyard_radius = lumberyard_radius

    def get_affordances(self, context: csf.core.Context) -> set[csf.core.Affordance]:
        affordances = set()

        perceptions = context.get_perceptions("WORKTIME")
        affordances.add(
            csf.core.Affordance(
                GoToLumberyard(self, self.__bot, self.__lumberyard_center, self.__lumberyard_radius),
                len(perceptions) * perceptions[0].value,
            )
        )

        if len(perceptions) * perceptions[0].value:
            perceptions = context.get_perceptions("IN_LUMBERYARD")
            if len(perceptions) > 0:
                affordances.add(
                    csf.core.Affordance(
                        GetRandomWood(self, self.__bot),
                        len(perceptions) * perceptions[0].value + 1,
                    )
                )

        return affordances


class GoToLumberyard(csf.practices.Practice):
    def __init__(self, creator, bot, yard_center, yard_radius) -> None:
        super().__init__(creator)
        self.__bot = bot
        self.__yard_center = yard_center
        self.__yard_radius = yard_radius

    def start(self) -> None:
        movement_goal = pathfinder.goals.GoalNearXZ(
            self.__yard_center.x, self.__yard_center.z, self.__yard_radius * 0.75
        )

        self.__bot.pathfinder.setGoal(movement_goal)
        self.change_state(csf.practices.Practice.State.RUNNING)

    def update(self) -> None:
        bot_position = self.__bot.entity.position
        if bot_position.distanceTo(self.__yard_center) < self.__yard_radius:
            self.change_state(csf.practices.Practice.State.FINISHED)
            return

    def exit(self) -> None:
        pass

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, GoToLumberyard):
            return __o.__yard_center == self.__yard_center and __o.__yard_radius == self.__yard_radius
        return False

    def __hash__(self) -> int:
        return hash((self.__yard_center, self.__yard_radius))


class GetRandomWood(csf.practices.Practice):
    def __init__(self, creator, bot) -> None:
        super().__init__(creator)
        self.__bot = bot

    def start(self) -> None:

        mcData = require("minecraft-data")(self.__bot.version)
        oak_id = mcData.blocksByName["oak_log"].id
        self.__target_block = self.__bot.findBlock({"matching": lambda block: block["type"] == oak_id})
        get_block_goal = pathfinder.goals.GoalBreakBlock(
            self.__target_block.position.x,
            self.__target_block.position.y,
            self.__target_block.position.z,
            self.__bot,
            {"range": 1},
        )

        self.__bot.pathfinder.setGoal(get_block_goal)
        self.change_state(csf.practices.Practice.State.RUNNING)

    def update(self) -> None:

        print(self.__target_block)
        bot_position = self.__bot.entity.position
        if bot_position.distanceTo(self.__target_block.position) < 2:
            if self.__target_block is not None:
                print("Start digging")
                self.__bot.dig(self.__target_block, "raycast")
                self.change_state(csf.practices.Practice.State.FINISHED)
                print("Stop digging")
                return

    def exit(self) -> None:
        pass

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, GetRandomWood):
            return True
        return False

    def __hash__(self) -> int:
        return hash(0)
