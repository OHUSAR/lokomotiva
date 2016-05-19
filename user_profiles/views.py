from django.contrib.auth.decorators import login_required
from user_profiles.forms import *
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from user_profiles.forms import UserForm
from events.api import get_events_for_user
from django.contrib.auth.decorators import user_passes_test


@login_required
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    all_users = User.objects.all().order_by('username')
    return render(request, 'lokoadmin/user_profiles/users.html', {'users': all_users})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_decider(request):
    return render(request, 'lokoadmin/user_profiles/user_decider.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_user(request, user_type):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            if user_type == 'trainer':
                UserType.objects.create(user=user, user_type=0)
            elif user_type == 'child':
                UserType.objects.create(user=user, user_type=1)
            elif user_type == 'parent':
                UserType.objects.create(user=user, user_type=2)
            return redirect(reverse("lokoadmin:user_profile", args=[user.pk]))
    else:
        form = UserForm()
    return render(request, 'lokoadmin/user_profiles/user_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    form = None

    user_events = get_events_for_user(user)

    if user.usertype.user_type == 1:
        child = None
        if ChildProfile.objects.filter(user=user).exists():
            child = ChildProfile.objects.get(user=user)
        form = ChildProfileForm(instance=child)
        if request.method == 'POST':
            form = ChildProfileForm(request.POST, instance=child)
            if form.is_valid():
                if child:
                    form.save()
                else:
                    child = form.save(commit=False)
                    child.user = user; child.save()

    elif user.usertype.user_type == 2:
        parent = None
        if ParentChildren.objects.filter(user=user).exists():
            parent = ParentChildren.objects.get(user=user)
        form = ParentChildrenForm(instance=parent)
        if request.method == 'POST':
            form = ParentChildrenForm(request.POST, instance=parent)
            if form.is_valid():
                if parent:
                    form.save()
                else:
                    parent = form.save(commit=False)
                    parent.user = user; parent.save()

    context = {'user': user, 'form': form, 'user_events': user_events}
    return render(request, 'lokoadmin/user_profiles/user_profile.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse("lokoadmin:user_profile", args=[pk]))
    else:
        form = UserEditForm(instance=user)
    return render(request, 'lokoadmin/user_profiles/user_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect(reverse("lokoadmin:users"))
    return render(request, 'lokoadmin/user_profiles/delete.html', {'user': user})
