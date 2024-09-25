from transaction_states_abc import TransactionState


class PendingState(TransactionState):
    def process(self, transaction) -> None:
        print(f"Transaction {transaction.transaction_id} is currently being processed.")


    def complete(self, transaction) -> None:
        print(f"Transaction {transaction.transaction_id} completed successfully.")
        transaction.change_state(CompletedState())


    def fail(self, transaction) -> None:
        print(f"Transaction {transaction.transaction_id} failed during processing.")
        transaction.change_state(FailedState())


class CompletedState(TransactionState):
    def process(self, transaction) -> None:
        print(f"Transaction {transaction.transaction_id} is already completed.")


    def complete(self, transaction) -> None:
        print(f"Transaction {transaction.transaction_id} is already in completed state.")


    def fail(self, transaction) -> None:
        print(f"Cannot fail transaction {transaction.transaction_id} because it is already completed.")


class FailedState(TransactionState):
    def process(self, transaction) -> None:
        print(f"Transaction {transaction.transaction_id} cannot be processed because it has failed.")


    def complete(self, transaction) -> None:
        print(f"Cannot complete transaction {transaction.transaction_id} because it has failed.")


    def fail(self, transaction) -> None:
        print(f"Transaction {transaction.transaction_id} is already in failed state.")