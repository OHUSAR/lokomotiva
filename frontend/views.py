from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from events.api import *
from django.utils import timezone


@login_required
def dashboard(request, wanted=0, type='all'):
    if request.POST:
        type = request.POST.get('type', 'all')

    wanted = int(wanted)
    start_date, end_date = get_month_interval(wanted)
    desired_events = get_events(start_date, end_date, type)
    interval = get_string_interval(start_date, end_date)

    context = {
        'events': desired_events,
        'older_link': wanted - 1,
        'newer_link': wanted + 1,
        'interval': interval,
        'type': type,
        'all_types': EventType.objects.all(),
    }
    return render(request, 'frontend/dashboard.html', context)


@login_required
def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    trainers, children, parents = get_attending_groups(event)

    current_attending = len(children) + len(parents)  # Trainers aren't limited by the capacity
    event_is_full = (current_attending >= event.max_capacity)
    signin_is_on = (timezone.now().date() <= event.signup_end_date)

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
                    msg = "Užívatel <b>{}</b> nie je na udalosť prihlásený.".format(
                        user.username
                    )
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


@login_required
def event_accomodations(request, pk):
    event = Event.objects.get(pk=pk)
    accomodations = event.accomodations
    trainers, children, parents = get_attending_groups(event)

    current_attending = len(children) + len(parents)  # Trainers aren't limited by the capacity
    event_is_full = (current_attending >= event.max_capacity)
    signin_is_on = (timezone.now().date() <= event.signup_end_date)

    msg = ""; color = "green"

    if request.method == 'POST':
        if signin_is_on:
            if 'sign_in' in request.POST or 'sign_out' in request.POST:
                user = User.objects.get(pk=int(request.POST['pk']))
                user_attending = is_attending(user, event)
                user_is_trainer = (user.usertype.user_type == 0)
                if 'sign_in' in request.POST:
                    if user_attending:
                        msg = "Užívatel <b>{}</b> už je na udalosť prihlásený.".format(
                            user.username
                        )
                        color = "red"
                    else:
                        if not user_is_trainer and event_is_full:
                            msg = "Prepáčte, táto udalosť je už plná."
                            color = "red"
                        else:
                            change_attending(user, event)
                            msg = "Užívatel <b>{}</b> bol úspešne prihlásený.".format(
                                user.username
                            )
                elif 'sign_out' in request.POST:
                    if not user_attending:
                        msg = "Užívatel <b>{}</b> nie je na udalosť prihlásený.".format(
                            user.username
                        )
                        color = "red"
                    else:
                        change_attending(user, event)
                        msg = "Užívatel <b>{}</b> bol úspešne odhlásený.".format(user.username)
            else:
                accomodation_pk = int([key for key in request.POST
                                       if key != 'csrfmiddlewaretoken' and key != 'users'][0])
                acc = Accomodation.objects.get(pk=accomodation_pk)
                user_pks = set(int(pk) for pk in request.POST.getlist('users', set()))
                my_users_pks = set(user.pk for user in get_users(request.user))
                print(acc, user_pks, my_users_pks)
                edit_group_accomodated(acc, user_pks, my_users_pks)
        else:
            msg = "Čas na prihlasovanie a odhlasovanie už vypršal."
            color = "red"

    my_users = get_users(request.user)  # all users curren user can sign_in (parents children)
    user_accomodation_going = dict()
    for a in accomodations.all():
        for u in my_users:
            user_accomodation_going['{}:{}'.format(a.pk, u.pk)] = is_accomodated(u, a)
    username_attending = [(u.username, is_attending(u, event)) for u in my_users]
    context = {
        'event': event,
        'accomodations': accomodations,
        'accomodation_stats': user_accomodation_going,
        'cur_cap': current_attending,
        'my_users': my_users,
        'my_users_stats': username_attending,
        'msg': msg,
        'color': color
    }
    return render(request, 'frontend/event_accomodations.html', context)
