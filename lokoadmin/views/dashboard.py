from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from events.models import Event
from django.shortcuts import render


@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_view(request):
    context = {
        'user_count': User.objects.all().count(),
        'event_count': Event.objects.all().count()
    }
    return render(request, 'lokoadmin/dashboard/dashboard.html', context)
