from oil.observer import ObservableEntity


class Equipment(ObservableEntity):
    def __init__(self, efficiency):
        super().__init__(
            lambda: dict(
                efficiency=efficiency
            )
        )


class Pump(Equipment):
    pass


class Wagon(Equipment):
    pass


class Drill(Equipment):
    pass
