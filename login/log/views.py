from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .forms import login_user,bio,registartion_user
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()


def get_login(request):
    return render(request,"login.html")



def logout_view(request):
    logout(request)
    return redirect('/index')

def register_view(request):
    title="Register"
    if request.method=='POST':
        print "feg"
        name=request.POST.get('name')
        email=request.POST.get('email')
        number=request.POST.get('mobile')
        password=request.POST.get('passwd')
        password2=request.POST.get('cpasswd')
        user_form=registartion_user({'username':name,'email':email,'password':password,'password2':password2})
        profile_form=bio({'number':number})
        if user_form.is_valid() and profile_form.is_valid():
            print "hkjmgh"
            user=user_form.save(commit=False)
            user2=profile_form.save(commit=False)
            password=user_form.cleaned_data.get('password')
            username=user_form.cleaned_data.get('username')
            user.set_password(password)
            user.save()
            user2.user = user
            user2.save()
            new_user = authenticate(username=username, password=password)
            login(request,new_user)
            return render(request,"index.html")
        else:
            return HttpResponse("fail")



