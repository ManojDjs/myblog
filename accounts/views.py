from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import userregistrationform,ProfileForm,userupdateform,profileupdateform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Logged in successfully! {username}!')
            return redirect('index')
        else:
            print('im here in else')
            messages.success(request, 'User name or password incorrect!')
            return redirect('login_user')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('you have been logged out'))
    return render(request, 'base.html')


def register_user(request):
    if request.method == 'POST':
        form = userregistrationform(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Sign up succesfull for {username}!')
            form.save()
            print('im here')
            return redirect('login_user')
    else:
        form = userregistrationform()
    return render(request, 'signup.html', {'form': form})


def index(request):
    return render(request, 'index.html')
@login_required
def profile(request):
    if request.method == "POST":
        u_form=userupdateform(request.POST,instance=request.user)
        p_form=profileupdateform(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            messages.success(request, f'Account is updated successfully!')
            u_form.save()
            p_form.save()
            print('im here')
            return redirect('profile')

    u_form = userupdateform(instance=request.user)
    p_form = profileupdateform(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    print('im in reqt image')

    return render(request,'profile.html',context)
