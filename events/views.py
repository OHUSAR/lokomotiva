from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from events.excel_utils import write_to_excel
from events.forms import EventTypeForm, EventForm, AccomodationForm, PaymentForm
from events.api import *


@user_passes_test(lambda u: u.is_superuser)
@login_required
def events(request, wanted=0, type="all"):
    if request.POST:
        type = request.POST.get('type', 'all')

    wanted = int(wanted)
    start_date, end_date = get_month_interval(wanted)
    desired_events = get_events(start_date, end_date, type)
    recent = get_string_interval(start_date, end_date)

    context = {
        'events': desired_events,
        'older_link': wanted - 1,
        'newer_link': wanted + 1,
        'recent': recent,
        'type': type,
        'all_types': EventType.objects.all(),
    }
    return render(request, 'lokoadmin/events/events.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def event_users(request, pk):
    event = Event.objects.get(pk=pk)
    msg = ""

    if request.method == 'POST':
        if 'excel' in request.POST:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(event.name)
            trainers_att, children_att, parents_att = get_attending_groups(event)
            xlsx_data = write_to_excel(event, trainers_att, children_att, parents_att)
            response.write(xlsx_data)
            return response

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


@user_passes_test(lambda u: u.is_superuser)
@login_required
def event_clone(request, pk):
    event = Event.objects.get(pk=pk)
    msg = ""; msg_color = "darkred"
    if request.method == 'POST':
        end_date = request.POST.get('end_date', None)
        day_count = request.POST.get('day_count', None)

        if not end_date or not day_count:
            msg = "Vyplňte obä polia."
        else:
            try:
                d, m, y = [int(thingy) for thingy in end_date.strip().split('-')]
                end_date = date(y, m, d)
                day_count = int(day_count.strip())

                count = clone_event(event, end_date, day_count)
                msg_color = "darkgreen"
                msg = "Tento event bol naklonovaný {} krát.".format(count)

            except (TypeError, ValueError) as error:
                msg = "Vyskytla sa chyba."
                print(error)

    context = {
        'msg': msg,
        'msg_color': msg_color,
        'event': event,
    }
    return render(request, 'lokoadmin/events/detail/event_clone.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def event_accomodation(request, pk, accomodation_pk=None):
    event = Event.objects.get(pk=pk)
    accomodations = Accomodation.objects.filter(event=event)
    msg = ""
    if accomodation_pk:
        accomodation = Accomodation.objects.get(pk=accomodation_pk)
        if request.method == 'POST':
            pks = set(int(k) for k, v in request.POST.items() if 'csrf' not in k)
            added, deleted = edit_user_accomodated(accomodation, pks)
            msg = "Pridaných: {} - Odobraných: {}".format(added, deleted)

    accomodation = ''
    trainers_att = []; trainers_not = []; children_att = []; children_not = []
    parents_att = []; parents_not = []; has_form = True
    if accomodation_pk:
        accomodation = Accomodation.objects.get(pk=accomodation_pk)
        trainers_att, children_att, parents_att = get_accomodated_groups(accomodation)
        trainers_not, children_not, parents_not = get_not_accomodated_groups(accomodation)
    else:
        has_form = False

    context = {
        'msg': msg,
        'event': event,
        'event_accomodations': accomodations,
        'active': accomodation,
        'has_form': has_form,
        'trainers_att': trainers_att,
        'trainers_not': trainers_not,
        'children_att': children_att,
        'children_not': children_not,
        'parents_att': parents_att,
        'parents_not': parents_not,
    }
    return render(request, 'lokoadmin/events/detail/event_accomodation.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def add_accomodation(request, pk):
    event = Event.objects.get(pk=pk)
    accomodations = Accomodation.objects.filter(event=event)
    if request.POST:
        form = AccomodationForm(request.POST)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.event = event
            new_acc.save()
    else:
        form = AccomodationForm()
    context = {
        'event': event,
        'event_accomodations': accomodations,
        'form': form,
    }
    return render(request, 'lokoadmin/events/detail/event_accomodation_add.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def edit_accomodation(request, pk, accomodation_pk):
    event = Event.objects.get(pk=pk)
    accomodations = Accomodation.objects.filter(event=event)
    accomodation = Accomodation.objects.get(pk=accomodation_pk)
    if request.POST:
        form = AccomodationForm(request.POST, instance=accomodation)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.event = event
            new_acc.save()
    else:
        form = AccomodationForm(instance=accomodation)

    context = {
        'event': event,
        'accomodation': accomodation,
        'active': accomodation.location,
        'event_accomodations': accomodations,
        'form': form,
    }
    return render(request, 'lokoadmin/events/detail/event_accomodation_add.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_accomodation(request, pk, accomodation_pk):
    Accomodation.objects.get(pk=accomodation_pk).delete()
    return redirect(reverse('lokoadmin:event_accomodation', args=[pk]))


@user_passes_test(lambda u: u.is_superuser)
@login_required
def event_payment(request, pk, payment_pk=None):
    event = Event.objects.get(pk=pk)
    all_payments = Payment.objects.filter(event=event)
    msg = ""
    if payment_pk:
        payment = Payment.objects.get(pk=payment_pk)
        if request.method == 'POST':
            pks = set(int(k) for k, v in request.POST.items() if 'csrf' not in k)
            added, deleted = edit_user_paid(payment, pks)
            msg = "Pridaných: {} - Odobraných: {}".format(added, deleted)

    payment = ''
    trainers_att = []; trainers_not = []; children_att = []; children_not = []
    parents_att = []; parents_not = []; has_form = True
    if payment_pk:
        payment = Payment.objects.get(pk=payment_pk)
        trainers_att, children_att, parents_att = get_paid_groups(payment)
        trainers_not, children_not, parents_not = get_not_paid_groups(payment)
    else:
        has_form = False

    context = {
        'msg': msg,
        'event': event,
        'event_payments': all_payments,
        'active': payment,
        'has_form': has_form,
        'trainers_att': trainers_att,
        'trainers_not': trainers_not,
        'children_att': children_att,
        'children_not': children_not,
        'parents_att': parents_att,
        'parents_not': parents_not,
    }
    return render(request, 'lokoadmin/events/detail/event_payment.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def add_payment(request, pk):
    event = Event.objects.get(pk=pk)
    all_payments = Payment.objects.filter(event=event)
    if request.POST:
        form = PaymentForm(request.POST)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.event = event
            new_acc.save()
    else:
        form = PaymentForm()

    context = {
        'event': event,
        'event_payments': all_payments,
        'form': form,
    }
    return render(request, 'lokoadmin/events/detail/event_payment_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def edit_payment(request, pk, payment_pk):
    event = Event.objects.get(pk=pk)
    all_payments = Payment.objects.filter(event=event)
    payment = Payment.objects.get(pk=payment_pk)
    if request.POST:
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.event = event
            new_acc.save()
    else:
        form = PaymentForm(instance=payment)

    context = {
        'event': event,
        'payment': payment,
        'active': payment,
        'event_payments': all_payments,
        'form': form,
    }
    return render(request, 'lokoadmin/events/detail/event_payment_form.html', context)


def delete_payment(request, pk, payment_pk):
    Payment.objects.get(pk=payment_pk).delete()
    return redirect(reverse('lokoadmin:event_payment', args=[pk]))


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
