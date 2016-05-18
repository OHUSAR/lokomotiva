from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from events.models import EventType


def events(request):
    return render(request, 'lokoadmin/events/events.html')


class EventTypeList(ListView):
    model = EventType
    template_name = 'lokoadmin/events/type_list.html'


class EventTypeAdd(CreateView):
    model = EventType
    fields = ['name']
    template_name = 'lokoadmin/events/type_add.html'


class EventTypeEdit(UpdateView):
    model = EventType
    fields = ['name']
    template_name = 'lokoadmin/events/type_add.html'


class EventTypeDelete(DeleteView):
    model = EventType
    success_url = reverse_lazy('lokoadmin:event_types')
    template_name = 'lokoadmin/events/type_delete.html'
