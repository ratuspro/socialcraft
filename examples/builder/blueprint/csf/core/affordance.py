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
