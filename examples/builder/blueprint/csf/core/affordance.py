class Affordance:
    def __init__(self, object, salience) -> None:
        self.__object = object
        self.__salience = salience

    @property
    def object(self):
        return self.__object

    @property
    def salience(self):
        return self.__salience

    def __str__(self) -> str:
        return f"{self.object} --- [salience: {self.salience}]"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Affordance):
            return self.__object == __o.object and self.__salience == __o.__salience
        return False

    def __hash__(self) -> int:
        return hash((self.__object, self.__salience))
