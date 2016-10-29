from events.api import get_users
from events.models import AttendingEvent, Payment, Paid


def get_unpaid_payments(user):
    users = get_users(user)
    total_unpaid = []
    for user in users:
        attending_events = set(ae.event for ae in AttendingEvent.objects.filter(user=user))

        existing_payments = set()
        for event in attending_events:
            existing_payments = existing_payments.union(
                set(p for p in Payment.objects.filter(event=event))
            )

        paid_payments = set(paid.payment for paid in Paid.objects.filter(user=user))

        for payment in existing_payments - paid_payments:
            total_unpaid.append((user, payment))

    return total_unpaid
