class Observer:
    def notify(self, observable, event):
        pass

    def observe(self, observable):
        observable.register_observer(self)


class Observable:
    def __init__(self):
        self.__dict__["observers"] = []

    def register_observer(self, observer):
        self.observers.append(observer)
        observer.notify(self, event=dict(action="new"))

    def notify_observers(self, event=dict()):
        for observer in self.observers:
            observer.notify(self, event)


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
