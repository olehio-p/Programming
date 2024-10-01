from datetime import datetime
from projects.project import Project
from projects.observers import ProjectObserver
from transactions.transaction import TransactionFactory
from transactions.payment_gateway import PaymentGateway, GatewayStatus

project = Project(
    project_id=1,
    user_id=123,
    title="Community Garden",
    description="A project to create a community garden.",
    goal_amount=5000.0,
    current_amount=1000.0,
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 12, 31),
    category_id=1,
    status="active"
)

project.add_observer(ProjectObserver("test_observer"))

paypal = PaymentGateway("PayPal", GatewayStatus.ACTIVE, 2.9)
stripe = PaymentGateway("Stripe", GatewayStatus.ACTIVE, 2.9)

donation = TransactionFactory.create_transaction(
    transaction_type="donation",
    user_id=456,
    project=project,
    amount=100.0,
    payment_gateway=paypal
)

print(donation)
donation.process()
donation.complete()

fee = TransactionFactory.create_transaction(
    transaction_type="fee",
    user_id=456,
    project=project,
    amount=50.0,
    payment_gateway=stripe
)


print(fee)
fee.process()
fee.complete()

withdrawal = TransactionFactory.create_transaction(
    transaction_type="withdrawal",
    user_id=456,
    project=project,
    amount=150.0,
    payment_gateway=paypal
)

print(withdrawal)
withdrawal.process()
withdrawal.fail()

print("\nFinal Project State:")
print(project)

print("\nTransaction Details:")
print(donation)
print(fee)
print(withdrawal)

