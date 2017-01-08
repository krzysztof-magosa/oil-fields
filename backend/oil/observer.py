# import queue
from itertools import groupby


class Group:
    def __init__(self):
        self.in_progress = False
        self.queue = []

    def assign(self, observable):
        observable.observer_group = self

    def assign_many(self, observables):
        for observable in observables:
            self.assign(observable)

    def begin(self):
        self.in_progress = True

    def commit(self):
        self.in_progress = False
        self._commit()

    def _commit(self):
        messages_grouped = groupby(
            sorted(
                self.queue,
                key=lambda x: hash(x[0])
            ),
            key=lambda x: x[0]
        )

        for observer, messages in messages_grouped:
            observer.notify([(x[1], x[2]) for x in messages])

    def notify(self, observer, observable, event):
        self.queue.append((observer, observable, event))

        if not self.in_progress:
            self._commit()


#
def by_observable(messages):
    messages_grouped = groupby(
        sorted(
            messages,
            key=lambda x: hash(x[0])
        ),
        key=lambda x: x[0]
    )

    for observable, messages_for_observable in messages_grouped:
        yield (observable, [x[1] for x in messages_for_observable])


class Observer:
    def notify(self, messages):
        pass

    def observe(self, observable, notify_new=True):
        observable.register_observer(self, notify_new)

    def observe_many(self, elements):
        for element in elements:
            self.observe(element)


class Observable:
    def __init__(self):
        self.__dict__["observers"] = set()
        self.__dict__["observer_group"] = Group()

    def register_observer(self, observer, notify_new=True):
        self.observers.add(observer)

        if notify_new:
            self.notify_observers(event=dict(action="new"))

    def notify_observers(self, event=dict()):
        for observer in self.observers:
            self.observer_group.notify(observer, self, event)


class ObservableEntity(Observable):
    def __init__(self):
        super().__init__()
        self.__dict__["data"] = dict()

    def __setattr__(self, name, value):
        if name in self.__dict__:
            object.__setattr__(self, name, value)
        else:
            self.data[name] = value
            self.notify_observers(
                dict(
                    action="update",
                    property=name
                )
            )

    def __getattr__(self, name):
        return self.__dict__["data"][name]
