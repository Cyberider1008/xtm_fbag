import re
from django import forms
from .models import *
from django.conf import settings

'''---------User Registration form created here---------'''


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.CharField(label='User name', required=True, max_length=60)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile_number')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @staticmethod
    def valid_email(email):
        if re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email) is not None:
            return True
        return False

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = user.email
        if commit:
            user.save()
        return user


'''---------------User change form created here-----------------------'''


class UserChangeForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].queryset = User.objects.exclude(email=kwargs['instance'].email)

    class Meta:
        model = User
        fields = '__all__'

    def clean_email(self):
        if hasattr(settings, 'VALIDATE_EMAIL') and settings.VALIDATE_EMAIL:
            if not self.valid_email(self.cleaned_data["email"]):
                raise forms.ValidationError("Please enter valid email")

        return self.cleaned_data["email"]

    @staticmethod
    def valid_email(email):
        if re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email) is not None:
            return True
        return False

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if user.email is None or user.email == '':
            user.email = user.email
            if commit:
                user.save()
        return






