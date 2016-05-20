from django.shortcuts import render
from events.api import *
from django.utils import timezone


def dashboard(request, wanted=0):
    """
    View of the index page of event_organize frontend.
    Page is showing upcoming events for one month (today + 30 days)

    :param request: HTML request by the user
    :param wanted: Users can browse through mohths. 0 is current month, +1 is older, -1 is newer
    :return: redered dashboard template with context
    """
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
    """
    View of event detail. Shows users that are attending and enables users to sign in.
    Parents can also sign in their children.

    :param request: HTML request by the user
    :param pk: ID of the viewed event
    :return: rendered event.html template
    """
    event = Event.objects.get(pk=pk)
    trainers, children, parents = get_attending_groups(event)

    current_attending = len(children) + len(parents)  # Trainers aren't limited by the capacity
    event_is_full = (current_attending >= event.max_capacity)
    signin_is_on = (timezone.now().date() <= event.signup_end_date or
                    timezone.now().time() <= event.signup_end_time)

    msg = ""; color = "green"

    if request.method == 'POST':
        if signin_is_on:
            user = User.objects.get(pk=int(request.POST['pk']))
            user_attending = is_attending(user, event)
            user_is_trainer = (user.usertype.user_type == 0)
            if 'sign_in' in request.POST:
                if user_attending:
                    msg = "Užívatel <b>{}</b> už je na udalosť prihlásený.".format(user.username)
                    color = "red"
                else:
                    if not user_is_trainer and event_is_full:
                        msg = "Prepáčte, táto udalosť je už plná."
                        color = "red"
                    else:
                        change_attending(user, event)
                        msg = "Užívatel <b>{}</b> bol úspešne prihlásený.".format(user.username)
            elif 'sign_out' in request.POST:
                if not user_attending:
                    msg = "Užívatel <b>{}</b> nie je na udalosť prihlásený.".format(user.username)
                    color = "red"
                else:
                    change_attending(user, event)
                    msg = "Užívatel <b>{}</b> bol úspešne odhlásený.".format(user.username)
        else:
            msg = "Čas na prihlasovanie a odhlasovanie už vypršal."
            color = "red"

    trainers, children, parents = get_attending_groups(event)
    my_users = get_users(request.user)  # all users curren user can sign_in (parents children)

    username_attending = [(u.username, is_attending(u, event)) for u in my_users]
    current_attending = len(children) + len(parents)

    context = {
        'event': event,
        'trainers': trainers,
        'children': children,
        'parents': parents,
        'cur_cap': current_attending,
        'my_users': my_users,
        'my_users_stats': username_attending,
        'msg': msg,
        'color': color
    }
    return render(request, 'frontend/event.html', context)
