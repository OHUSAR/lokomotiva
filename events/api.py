from events.models import *
from user_profiles.models import *
from datetime import date, timedelta


def get_events(start_date, end_date, type='all'):
    if type == 'all':
        return Event.objects.filter(start_date__range=[start_date, end_date])
    return Event.objects.filter(start_date__range=[start_date, end_date], type__name=type)


def get_month_interval(number):
    month = timedelta(days=30)
    start_date = date.today()
    if number > 0:
        for i in range(number):
            start_date += month
    else:
        for i in range(abs(number)):
            start_date -= month

    end_date = start_date + month

    return start_date, end_date


def get_string_interval(start_date, end_date):
    return "{}. {}. {} - {}. {}. {}".format(start_date.day, start_date.month, start_date.year,
                                            end_date.day, end_date.month, end_date.year)


def get_attending_groups(event):
    all_users = [ev.user for ev in AttendingEvent.objects.filter(event=event)]
    trainers = []; children = []; parents = []
    for user in all_users:
        if user.usertype.user_type == 1:
            children.append(user)
        elif user.usertype.user_type == 2:
            parents.append(user)
        else:
            trainers.append(user)

    return trainers, children, parents


def get_not_attending_groups(event):
    all_users = [u for u in User.objects.all() if not is_attending(u, event)]
    trainers = []; children = []; parents = []
    for user in all_users:
        if user.usertype.user_type == 1:
            children.append(user)
        elif user.usertype.user_type == 2:
            parents.append(user)
        else:
            trainers.append(user)

    return trainers, children, parents


def get_accomodated_groups(accomodation):
    all_users = [acc.user for acc in Accomodated.objects.filter(accomodation=accomodation)]
    trainers = []; children = []; parents = []
    for user in all_users:
        if user.usertype.user_type == 1:
            children.append(user)
        elif user.usertype.user_type == 2:
            parents.append(user)
        else:
            trainers.append(user)

    return trainers, children, parents


def get_not_accomodated_groups(accomodation):
    all_users = [u for u in User.objects.all() if not is_accomodated(u, accomodation)]
    trainers = []; children = []; parents = []
    for user in all_users:
        if user.usertype.user_type == 1:
            children.append(user)
        elif user.usertype.user_type == 2:
            parents.append(user)
        else:
            trainers.append(user)

    return trainers, children, parents


def has_paid(user, payment):
    return Paid.objects.filter(payment=payment, user=user).exists()


def get_paid_groups(payment):
    all_users = [acc.user for acc in Paid.objects.filter(payment=payment)]
    trainers = []; children = []; parents = []
    for user in all_users:
        if user.usertype.user_type == 1:
            children.append(user)
        elif user.usertype.user_type == 2:
            parents.append(user)
        else:
            trainers.append(user)

    return trainers, children, parents


def get_not_paid_groups(payment):
    all_users = [u for u in User.objects.all() if not has_paid(u, payment)]
    trainers = []; children = []; parents = []
    for user in all_users:
        if user.usertype.user_type == 1:
            children.append(user)
        elif user.usertype.user_type == 2:
            parents.append(user)
        else:
            trainers.append(user)

    return trainers, children, parents


def get_users(user):
    if user.usertype.user_type != 2:
        return [user]
    users = [user]
    for child in ParentChildren.objects.get(user=user).children.all():
        users.append(child.user)
    return users


def get_events_for_user(user):
    return [record.event for record in AttendingEvent.objects.filter(user=user)]


def is_attending(user, event):
    return AttendingEvent.objects.filter(user=user, event=event).exists()


def is_accomodated(user, accomodation):
    return Accomodated.objects.filter(user=user, accomodation=accomodation).exists()


def change_attending(user, event):
    if AttendingEvent.objects.filter(user=user, event=event).exists():
        AttendingEvent.objects.get(user=user, event=event).delete()
    else:
        AttendingEvent.objects.create(user=user, event=event)


def change_accomodated(user, event):
    if Accomodated.objects.filter(user=user, event=event).exists():
        Accomodated.objects.get(user=user, event=event).delete()
    else:
        Accomodated.objects.create(user=user, event=event)


def edit_user_attending(event, user_pks):
    added = deleted = 0
    all_user_pks = set(u.pk for u in User.objects.all())
    attending_pks = set(att.user.pk for att in AttendingEvent.objects.filter(event=event))
    not_att_pks = all_user_pks - attending_pks

    for add_att_pk in (user_pks & not_att_pks):
        added += 1
        user = User.objects.get(pk=add_att_pk)
        AttendingEvent.objects.create(event=event, user=user)

    for remove_att_pk in (attending_pks - user_pks):
        deleted += 1
        user = User.objects.get(pk=remove_att_pk)
        AttendingEvent.objects.get(event=event, user=user).delete()

    return added, deleted


def edit_user_paid(payment, user_pks):
    added = deleted = 0
    all_user_pks = set(u.pk for u in User.objects.all())
    users_paid = set(att.user.pk for att in Paid.objects.filter(payment=payment))
    not_acc_pks = all_user_pks - users_paid

    for add_att_pk in (user_pks & not_acc_pks):
        added += 1
        user = User.objects.get(pk=add_att_pk)
        Paid.objects.create(payment=payment, user=user)

    for remove_att_pk in (users_paid - user_pks):
        deleted += 1
        user = User.objects.get(pk=remove_att_pk)
        Paid.objects.get(payment=payment, user=user).delete()

    return added, deleted


def edit_user_accomodated(accomodation, user_pks):
    added = deleted = 0
    all_user_pks = set(u.pk for u in User.objects.all())
    accomodated_pks = set(att.user.pk for att in
                          Accomodated.objects.filter(accomodation=accomodation))
    not_acc_pks = all_user_pks - accomodated_pks

    for add_att_pk in (user_pks & not_acc_pks):
        added += 1
        user = User.objects.get(pk=add_att_pk)
        Accomodated.objects.create(accomodation=accomodation, user=user)

    for remove_att_pk in (accomodated_pks - user_pks):
        deleted += 1
        user = User.objects.get(pk=remove_att_pk)
        Accomodated.objects.get(accomodation=accomodation, user=user).delete()

    return added, deleted


def edit_group_accomodated(accomodation, user_pks, all_user_pks):
    added = deleted = 0
    accomodated_pks = set(att.user.pk for att in
                          Accomodated.objects.filter(accomodation=accomodation))
    not_acc_pks = all_user_pks - accomodated_pks

    for add_att_pk in (user_pks & not_acc_pks):
        added += 1
        user = User.objects.get(pk=add_att_pk)
        Accomodated.objects.create(accomodation=accomodation, user=user)

    for remove_att_pk in (accomodated_pks - user_pks):
        deleted += 1
        user = User.objects.get(pk=remove_att_pk)
        Accomodated.objects.get(accomodation=accomodation, user=user).delete()

    return added, deleted


def clone_event(event, end_date, day_count):
    day_shift = timedelta(days=day_count)
    current_shift = day_shift
    count = 0
    while event.start_date + current_shift < end_date:
        count += 1
        current_shift += day_shift

        new_event = Event(
            type=event.type,
            name=event.name,
            location=event.location,
            start_date=event.start_date + current_shift,
            end_date=event.end_date + current_shift,
            start_time=event.start_time,
            end_time=event.end_time,
            description=event.description,
            max_capacity=event.max_capacity,
            signup_end_date=event.signup_end_date + current_shift,
            signup_end_time=event.signup_end_time,
        )
        new_event.full_clean(); new_event.save()

    return count
