from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate
from django.contrib import messages

from .forms import userRegisterForm, UserUpdateForm, profileUpdateForm

from django.contrib.auth.decorators import login_required


def register(request):
    form = userRegisterForm()

    if request.method =='POST':
        form = userRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')

            messages.success(request, f'Your Account Has Been Created!')

            # user = authenticate
            
            
            return redirect('login')
    else:
        form = userRegisterForm()

    context = {'form':form}
    return render(request, 'users/register.html', context)


@login_required(login_url='login')
def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = profileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your Account Has Been Updated!')

            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

    context = {'u_form':u_form, 'p_form':p_form}
    return render(request, 'users/profile.html',context)