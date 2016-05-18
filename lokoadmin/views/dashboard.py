from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


@login_required
def dashboard_view(request):
    context = {
        'user_count': User.objects.all().count()
    }
    return render(request, 'lokoadmin/dashboard/dashboard.html', context)
