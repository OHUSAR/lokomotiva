from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from events.models import *
from events.forms import EventTypeForm, EventForm
from events.api import get_events, get_month_interval, get_string_interval


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


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
@method_decorator(login_required, name='dispatch')
class EventDetail(DeleteView):
    model = Event
    template_name = 'lokoadmin/events/event_detail.html'


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
