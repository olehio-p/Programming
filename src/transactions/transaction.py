from datetime import datetime
from typing import Optional
import uuid

from .payment_gateway import PaymentGateway
from projects.project import Project
from .transaction_states import PendingState
from .transaction_states_abc import TransactionState


class Transaction:
    def __init__(
        self,
        user_id: int,
        project: Project,
        transaction_type: str,
        amount: float,
        payment_gateway: PaymentGateway,
        date: Optional[datetime] = None,
        state: Optional[TransactionState] = None
    ) -> None:
        self._transaction_id: str = str(uuid.uuid4())
        self._user_id: int = user_id
        self._project: Project = project
        self._transaction_type: str = transaction_type
        self._amount: float = amount
        self._payment_gateway: PaymentGateway = payment_gateway
        self._date: datetime = date if date is not None else datetime.now()
        self._state: TransactionState = state if state is not None else PendingState()

    @property
    def transaction_id(self) -> str:
        return self._transaction_id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def project(self) -> Project:
        return self._project

    @property
    def transaction_type(self) -> str:
        return self._transaction_type

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def payment_gateway(self) -> PaymentGateway:
        return self._payment_gateway

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def state(self) -> str:
        return self._state.__class__.__name__

    def change_state(self, new_state: TransactionState) -> None:
        self._state = new_state
        print(f"Transaction {self.transaction_id} changed to state: {self.state}")

    def process(self) -> None:
        self._state.process(self)

    def complete(self) -> None:
        if self._transaction_type == "donation":
            self._project.adjust_amount(self._amount)
        elif self._transaction_type == "withdrawal":
            self._project.adjust_amount(-self._amount)
        elif self._transaction_type == "fee":
            self._project.adjust_amount(-self._amount)
        self._state.process(self)
        print(f"Transaction {self.transaction_id} processed. Project new amount: {self._project.current_amount}")
        self._state.complete(self)

    def fail(self) -> None:
        self._state.fail(self)

    def __str__(self) -> str:
        return (f"Transaction(ID: {self.transaction_id}, User ID: {self.user_id}, "
                f"Project: {self.project.title}, Type: {self.transaction_type}, "
                f"Amount: {self.amount:.2f}, Payment Gateway: {self.payment_gateway}, "
                f"Date: {self.date}, State: {self.state})")


class DonationTransaction(Transaction):
    def __init__(self, user_id: int, project: Project, transaction_type: str, amount: float, payment_gateway: PaymentGateway) -> None:
        super().__init__(user_id=user_id, project=project, transaction_type=transaction_type,
                         amount=amount, payment_gateway=payment_gateway)


class FeeTransaction(Transaction):
    def __init__(self, user_id: int, project: Project, transaction_type: str, amount: float, payment_gateway: PaymentGateway) -> None:
        super().__init__(user_id=user_id, project=project, transaction_type=transaction_type,
                         amount=amount, payment_gateway=payment_gateway)


class WithdrawalTransaction(Transaction):
    def __init__(self, user_id: int, project: Project, transaction_type: str, amount: float, payment_gateway: PaymentGateway) -> None:
        super().__init__(user_id=user_id, project=project, transaction_type=transaction_type,
                         amount=amount, payment_gateway=payment_gateway)


class TransactionFactory:
    @staticmethod
    def create_transaction(transaction_type: str, user_id: int, project: Project,
                           amount: float, payment_gateway: PaymentGateway) -> Transaction:
        if transaction_type == "donation":
            return DonationTransaction(user_id, project, transaction_type, amount, payment_gateway)
        elif transaction_type == "fee":
            return FeeTransaction(user_id, project, transaction_type, amount, payment_gateway)
        elif transaction_type == "withdrawal":
            return WithdrawalTransaction(user_id, project, transaction_type, amount, payment_gateway)
        else:
            raise ValueError(f"Unknown transaction type: {transaction_type}")