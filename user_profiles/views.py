from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from user_profiles.forms import UserForm


@login_required
def users(request):
    all_users = User.objects.all()
    return render(request, 'lokoadmin/user_profiles/users.html', {'users': all_users})


@login_required
def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect(reverse("lokoadmin:dashboard"))
    else:
        form = UserForm()
    return render(request, 'lokoadmin/user_profiles/add_user.html', {'form': form})
