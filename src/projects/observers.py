from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass


class ProjectObserver(Observer):
    def __init__(self, recipient: str):
        self._recipient = recipient

    @property
    def recipient(self):
        return self._recipient

    def update(self, message: str):
        print(f"Notification to {self._recipient}: {message}")


class Observable:
    def __init__(self):
        super().__init__()
        self._observers = []


    def add_observer(self, observer: Observer):
        self._observers.append(observer)


    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)


    def notify_observers(self, message: str):
        for observer in self._observers:
            observer.update(message)