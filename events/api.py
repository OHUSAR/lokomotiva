from events.models import *
from user_profiles.models import *
from datetime import date, timedelta


def get_events(start_date, end_date):
    return Event.objects.filter(start_date__range=[start_date, end_date])


def get_month_interval(number):
    month = timedelta(days=30)
    start_date = date.today() - month
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


def change_attending(user, event):
    if AttendingEvent.objects.filter(user=user, event=event).exists():
        AttendingEvent.objects.get(user=user, event=event).delete()
    else:
        AttendingEvent.objects.create(user=user, event=event)
