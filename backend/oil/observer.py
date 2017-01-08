from collections import defaultdict
from itertools import groupby
import uuid


def observe_elements(observer, group_name, elements):
    group = ObservableGroup(name=group_name)
    group.begin()
    group.register_observer(observer)

    for element in elements:
        group.own(element)
        observer.observe(element)

    group.commit()


class Observer:
    def notify(self, group, events):
        pass

    def observe(self, observable, notify_new=True):
        observable.register_observer(self, notify_new)


class ObservableGroup:
    def __init__(self, name=str(uuid.uuid4())):
        self.name = name
        self.auto_commit = True
        self.observers = set()
        self.messages = []

    def begin(self):
        self.auto_commit = False

    def commit(self):
        data = sorted(self.messages, key=lambda x: hash(x[0]))

        for observer in self.observers:
            observer.notify(self, self.messages)

        self.messages = []
        self.auto_commit = True

    def notify(self, observable, event):
        self.messages.append((observable, event))

        if self.auto_commit:
            self.commit()

    def own(self, element):
        element.observable_group = self
        # @@@ transfer messages to new group

    def register_observer(self, observer):
        self.observers.add(observer)


class Observable:
    def __init__(self):
        self.__dict__["observable_group"] = ObservableGroup()

    def register_observer(self, observer, notify_new=True):
        self.observable_group.register_observer(observer)

        if notify_new:
            self.observable_group.notify(self, event=dict(action="new"))

#    def notify_observers(self, event=dict()):
#        self.observable_group.notify(self, event=event)


class ObservableEntity(Observable):
    def __init__(self):
        super().__init__()
        self.__dict__["data"] = dict()

    def __setattr__(self, name, value):
        if name in self.__dict__:
            object.__setattr__(self, name, value)
        else:
            self.data[name] = value
            self.observable_group.notify(
                self,
                dict(
                    action="update",
                    property=name
                )
            )

    def __getattr__(self, name):
        return self.__dict__["data"][name]
