import uuid
from oil.equipment import Pump, Wagon, Drill
from oil.observer import ObservableEntity


class Estate(ObservableEntity):
    def __init__(self, name, price):
        super().__init__()
        self.uuid = uuid.uuid4()
        self.name = name
        self.price = price
        self.owner = None

    @property
    def api_data(self):
        return dict(
            name=self.name,
            uuid=str(self.uuid),
            type=self.__class__.__name__.lower(),
            price=self.price,
            owner=(str(self.owner.uuid) if self.owner else None)
        )

    def produce(self):
        raise NotImplementedError()


class Oilfield(Estate):
    def __init__(self, name, price, efficiency, capacity, deposit_depth, drill_progress):
        """
        efficiency     - how many liters per cycle
        capacity       - how many liters in total
        deposit_depth  - how deep the oil is placed
        drill_progress - maximum drill progress per cycle
        """
        super().__init__(name, price)
        self.efficiency = efficiency
        self.capacity = capacity
        self.deposit_depth = deposit_depth
        self.current_depth = 0
        self.drill_progress = drill_progress
        self.oil = 0
        self.equipments = []

    @property
    def api_data(self):
        return dict(
            **super().api_data,
            current_depth=self.current_depth,
            equipments_count=dict(
                drill=len([x for x in self.equipments if isinstance(x, Drill)]),
                pump=len([x for x in self.equipments if isinstance(x, Pump)]),
                wagon=len([x for x in self.equipments if isinstance(x, Wagon)])
            ),
            oil=self.oil
        )

    def equipments_by_type(self, type=None):
        return (x for x in self.equipments if isinstance(x, type))

    def open(self):
        return self.current_depth >= self.deposit_depth

    def drill(self):
        if self.open() or not self.owner:
            return

        remaining = min(
            self.drill_progress,                     # how much we can progress per cycle
            self.deposit_depth - self.current_depth  # how much we need
        )
        for drill in self.equipments_by_type(Drill):
            step = min(drill.efficiency, remaining)
            remaining -= step
            drill.efficiency -= step
            self.current_depth += step

    def pump(self):
        if not self.open() or not self.owner:
            return

        amount = min(
            self.efficiency,  # how much per cycle
            self.capacity,    # how much we have in oilfield
            sum((x.efficiency for x in self.equipments_by_type(Pump))) # how much we can pump
        )

        self.capacity -= amount
        self.oil += amount

    def transport(self):
        if not self.open() or not self.owner:
            return

        amount = min(
            sum((x.efficiency for x in self.equipments_by_type(Wagon))), # how much we can take at once
            self.oil # what we have
        )

        self.oil -= amount
        self.owner.oil += amount

    def produce(self):
        self.drill()
        self.pump()
        self.transport()


class Factory(Estate):
    def __init__(self, name, price, efficiency, equipment, spec):
        super().__init__(name, price)

        self.efficiency = efficiency
        self.equipment = equipment
        self.spec = spec
        self.equipment_price = 0
        self.stock = []

    @property
    def api_data(self):
        return dict(
            **super().api_data,
            equipment_price=self.equipment_price,
            stock=len(self.stock)
        )

    def produce(self):
        if self.owner:
            for i in range(self.efficiency):
                self.store(self.equipment(**self.spec))

    def deliver(self, amount, oilfield):
        for _ in range(min(amount, len(self.stock))):
            item = self.stock.pop()
            oilfield.equipments.append(item)
            oilfield.owner.balance -= self.equipment_price

        self.observable_group.notify(
            self,
            dict(action="update", property="stock")
        )

    def store(self, equipment):
        self.stock.append(equipment)
        self.observable_group.notify(
            self,
            dict(action="update", property="stock")
        )


class PumpFactory(Factory):
    def __init__(self, name, price, efficiency, spec):
        super().__init__(
            name=name,
            price=price,
            efficiency=efficiency,
            equipment=Pump,
            spec=spec
        )


class WagonFactory(Factory):
    def __init__(self, name, price, efficiency, spec):
        super().__init__(
            name=name,
            price=price,
            efficiency=efficiency,
            equipment=Wagon,
            spec=spec
        )


class DrillFactory(Factory):
    def __init__(self, name, price, efficiency, spec):
        super().__init__(
            name=name,
            price=price,
            efficiency=efficiency,
            equipment=Drill,
            spec=spec
        )
