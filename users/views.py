from django.shortcuts import redirect, render
from users.forms import EditUserForm, UserForm, UserProfileInfoForm
from django.urls import reverse
from users.models import UserProfileInfo

from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.
def index(request):
    return render(request, 'users/index.html')


def registerView(request):
    registered = False  # flag to check if user is registered
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            password = user_form.cleaned_data.get('password')

            try:
                validate_password(password) # validate password
            except ValidationError as e:
                user_form.add_error('password', e) # add error to form
                return render(request, 'users/register.html', {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered
                })
            
            # save user and profile
            user = user_form.save(commit=False)
            user.set_password(password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('users:index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print(f"Username: {username} and password {password}")

            return HttpResponse("invalid login details supplied!")
        
    else:
        return render(request, 'users/login_logout.html', {})

@login_required
def logoutView(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('users:index'))
    return render(request, 'users/login_logout.html', {})

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_profile(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    user = request.user 
    profile = user.userprofileinfo

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)  
        profile_form = UserProfileInfoForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            print(request, 'Your profile has been updated successfully!')
            return redirect('edit_profile')
        else:
            print(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileInfoForm(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

def edit_profile(request):
    user = request.user

    if user.is_superuser:
        # TODO Has no userprofileinfo object to edit 
        return redirect('admin:index')

    profile = user.userprofileinfo


    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = UserProfileInfoForm(request.POST, request.FILES, instance=profile) 

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = EditUserForm(instance=user)
        profile_form = UserProfileInfoForm(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
