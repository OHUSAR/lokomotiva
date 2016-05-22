from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from events.forms import EventTypeForm, EventForm
from events.api import *


@user_passes_test(lambda u: u.is_superuser)
@login_required
def events(request, wanted=0):
    wanted = int(wanted)
    start_date, end_date = get_month_interval(wanted)
    desired_events = get_events(start_date, end_date)
    recent = get_string_interval(start_date, end_date)

    context = {
        'events': desired_events,
        'older_link': wanted - 1,
        'newer_link': wanted + 1,
        'recent': recent
    }
    return render(request, 'lokoadmin/events/events.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def event_users(request, pk):
    event = Event.objects.get(pk=pk)
    msg = ""
    if request.method == 'POST':
        pks = set(int(k) for k, v in request.POST.items() if 'csrf' not in k)
        added, deleted = edit_user_attending(event, pks)
        msg = "Pridaných: {} - Odobraných: {}".format(added, deleted)

    trainers_att, children_att, parents_att = get_attending_groups(event)
    trainers_not, children_not, parents_not = get_not_attending_groups(event)
    capacity = "{} / {}".format(len(children_att) + len(parents_att), event.max_capacity)
    context = {
        'event': event,
        'trainers_att': trainers_att,
        'trainers_not': trainers_not,
        'children_att': children_att,
        'children_not': children_not,
        'parents_att': parents_att,
        'parents_not': parents_not,
        'msg': msg,
        'capacity': capacity
    }
    return render(request, 'lokoadmin/events/detail/event_users.html', context)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EventDetail(DeleteView):
    model = Event
    template_name = 'lokoadmin/events/detail/event_detail.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EventAdd(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'lokoadmin/events/event_form.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EventEdit(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'lokoadmin/events/event_form.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('lokoadmin:events')
    template_name = 'lokoadmin/events/event_delete.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EventTypeList(ListView):
    model = EventType
    template_name = 'lokoadmin/events/type_list.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EventTypeAdd(CreateView):
    model = EventType
    form_class = EventTypeForm
    template_name = 'lokoadmin/events/type_add.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EventTypeEdit(UpdateView):
    model = EventType
    form_class = EventTypeForm
    template_name = 'lokoadmin/events/type_add.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EventTypeDelete(DeleteView):
    model = EventType
    success_url = reverse_lazy('lokoadmin:event_types')
    template_name = 'lokoadmin/events/type_delete.html'
