from enum import Enum

class GatewayStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class PaymentGateway:
    def __init__(self, name: str, status: GatewayStatus, transaction_fee: float):
        self._name = name
        self._status = status
        self._transaction_fee = transaction_fee


    @property
    def name(self) -> str:
        return self._name


    @property
    def status(self) -> GatewayStatus:
        return self._status


    @property
    def transaction_fee(self) -> float:
        return self._transaction_fee


    @status.setter
    def status(self, new_status: GatewayStatus) -> None:
        self._status = new_status


    @transaction_fee.setter
    def transaction_fee(self, new_fee: float) -> None:
        if new_fee < 0:
            raise ValueError("Transaction fee cannot be negative.")
        self._transaction_fee = new_fee

    def is_active(self) -> bool:
        return self._status == GatewayStatus.ACTIVE

    def __str__(self) -> str:
        return (f"{self.name} (Status: {self.status.value}, "
                f"Fee: {self.transaction_fee:.2f}%)")
