from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from events.models import Event
from django.shortcuts import render
from datetime import date, timedelta


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_view(request):
    today = date.today() - timedelta(days=1)
    one_year_from_today = today + timedelta(days=365)
    most_recent_event_pk = ""
    if Event.objects.filter(start_date__range=[today, one_year_from_today]).exists():
        event = Event.objects.filter(start_date__range=[today, one_year_from_today])[0]
        most_recent_event_pk = event.pk

    context = {
        'user_count': User.objects.all().count(),
        'event_count': Event.objects.all().count(),
        'most_recent_event_pk': most_recent_event_pk
    }
    return render(request, 'lokoadmin/dashboard/dashboard.html', context)
