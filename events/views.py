from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from events.models import *
from events.forms import EventTypeForm, EventForm
from datetime import date, timedelta


def events(request):
    startdate = date.today()
    enddate = startdate + timedelta(days=30)
    recent_events = Event.objects.filter(start_date__range=[startdate, enddate])
    context = {
        'events': recent_events
    }
    return render(request, 'lokoadmin/events/events.html', context)


class EventDetail(DeleteView):
    model = Event
    template_name = 'lokoadmin/events/event_detail.html'


class EventAdd(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'lokoadmin/events/event_form.html'


class EventEdit(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'lokoadmin/events/event_form.html'


class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('lokoadmin:events')
    template_name = 'lokoadmin/events/event_delete.html'


class EventTypeList(ListView):
    model = EventType
    template_name = 'lokoadmin/events/type_list.html'


class EventTypeAdd(CreateView):
    model = EventType
    form_class = EventTypeForm
    template_name = 'lokoadmin/events/type_add.html'


class EventTypeEdit(UpdateView):
    model = EventType
    form_class = EventTypeForm
    template_name = 'lokoadmin/events/type_add.html'


class EventTypeDelete(DeleteView):
    model = EventType
    success_url = reverse_lazy('lokoadmin:event_types')
    template_name = 'lokoadmin/events/type_delete.html'
