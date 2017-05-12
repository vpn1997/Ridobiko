from django import forms
from log.models import UserProfile
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
User=get_user_model()

class login_user(forms.Form):
    username= forms.CharField(max_length=None,label="Username")
    password= forms.CharField(max_length=None,widget=forms.PasswordInput,label="Passward")

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
             user = authenticate(username=username,password=password)
             if not user:
                raise forms.ValidationError("This user doesnot exist")
             if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
        return super(login_user,self).clean()



class registartion_user(forms.ModelForm):
    password = forms.CharField(max_length=None, widget=forms.PasswordInput, label="Passward")
    password2 = forms.CharField(max_length=None, widget=forms.PasswordInput, label="Passward Conform")
    class Meta:
        model = User
        fields=[
            'username',
            'email',
            'password',
            'password2'
        ]

        def clean_password2(self):
            passw=self.clean_data.get('password')
            passw2 = self.clean_data.get('password2')
            if passw != passw2:
                raise forms.ValidationError("Passwords must match")
            eml=self.clean_data.get('email')
            email_qs = User.objects.filter(email=eml)
            if email_qs.exists():
                raise forms.ValidationError("Email already exists")
            return passw


class bio(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['number']


