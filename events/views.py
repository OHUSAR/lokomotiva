from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from events.models import EventType


def events(request):
    return render(request, 'lokoadmin/events/events.html')


class EventTypeList(ListView):
    model = EventType


class EventTypeAdd(CreateView):
    model = EventType


class EventTypeEdit(UpdateView):
    model = EventType


class EventTypeDelete(DeleteView):
    model = EventType
