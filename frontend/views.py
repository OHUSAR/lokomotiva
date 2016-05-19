from django.shortcuts import render
from events.api import *
from django.utils import timezone


def dashboard(request, wanted=0):
    wanted = int(wanted)
    start_date, end_date = get_month_interval(wanted)
    desired_events = get_events(start_date, end_date)
    interval = get_string_interval(start_date, end_date)

    context = {
        'events': desired_events,
        'older_link': wanted + 1,
        'newer_link': wanted - 1,
        'interval': interval
    }
    return render(request, 'frontend/dashboard.html', context)


def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    trainers, children, parents = get_attending_groups(event)
    current_attending = len(children) + len(parents)
    is_full = ""
    if request.method == 'POST':
        user = User.objects.get(pk=int(request.POST['pk']))
        if (current_attending >= event.max_capacity and
                not is_attending(user, event) and
                user.usertype.user_type != 0):
            is_full = "Prepáčte, táto udalosť je už plná."
        else:
            change_attending(user, event)

    trainers, children, parents = get_attending_groups(event)
    my_users = get_users(request.user)

    current_attending = len(children) + len(parents)
    disabled = (timezone.now().date() > event.signup_end_date and
                timezone.now().time() > event.signup_end_time)
    context = {
        'event': event,
        'trainers': trainers,
        'children': children,
        'parents': parents,
        'cur_cap': current_attending,
        'my_users': my_users,
        'disabled': disabled,
        'is_full': is_full
    }
    return render(request, 'frontend/event.html', context)
