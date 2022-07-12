from django.contrib.auth import forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


# User Login Form (Applied in both student and instructor login)
class MyUserCreationForm(forms.UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        error_messages = {
            "username": {"unique": ("This username has already been taken.")}
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'username', 'email', 'bio']
