from abc import ABC, abstractmethod


class TransactionState(ABC):
    @abstractmethod
    def process(self, transaction) -> None:
        pass

    @abstractmethod
    def complete(self, transaction) -> None:
        pass

    @abstractmethod
    def fail(self, transaction) -> None:
        pass