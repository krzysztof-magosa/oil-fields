# import queue
from itertools import groupby


during_transaction = False
message_queue = []  # queue.Queue()


def begin_transaction():
    global during_transaction
    during_transaction = True


def commit_transaction():
    global during_transaction
    during_transaction = False
    _commit()


def _commit():
    global message_queue
    # grouped by observer.
    messages_grouped = groupby(
        sorted(
            message_queue,
            key=lambda x: hash(x[0])
        ),
        key=lambda x: x[0]
    )

    for observer, messages in messages_grouped:
        observer.notify([(x[1], x[2]) for x in messages])


def notify(observer, observable, event):
    global message_queue
    global during_transaction

    message_queue.append((observer, observable, event))

    if not during_transaction:
        _commit()


#
def observe_elements(observer, elements):
    for element in elements:
        observer.observe(element)


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


class Observable:
    def __init__(self):
        self.__dict__["observers"] = set()

    def register_observer(self, observer, notify_new=True):
        self.observers.add(observer)

        if notify_new:
            self.notify_observers(event=dict(action="new"))

    def notify_observers(self, event=dict()):
        for observer in self.observers:
            notify(observer, self, event)


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
