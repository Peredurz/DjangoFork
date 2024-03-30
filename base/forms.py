from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from .models import Profile, Collection, Medicine
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
)
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    error_messages = {
        "invalid_login": "Please enter a correct %(username)s and password. Note that both fields may be case-sensitive."
    }

    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["city", "date_of_birth", "bioText"]
        widgets = {
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "bioText": forms.Textarea(attrs={"class": "form-control"}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class CollectionForm(forms.ModelForm):
    medition = forms.ModelChoiceField(
        queryset=Medicine.objects.all(),
        empty_label="Select a medicine",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    userID = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Select a user",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        required=True,
    )

    class Meta:
        model = Collection
        fields = ["medition", "userID", "date"]

    def __init__(self, *args, **kwargs):
        initial_medition = kwargs.pop("initial_medition", None)
        super().__init__(*args, **kwargs)
        if initial_medition:
            self.fields["medition"].initial = initial_medition


class approveTimeForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ("collectedApproved",)
        widgets = {
            "collectedApproved": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "manufacturer", "cures", "sideEffects"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "manufacturer": forms.TextInput(attrs={"class": "form-control"}),
            "cures": forms.TextInput(attrs={"class": "form-control"}),
            "sideEffects": forms.Textarea(attrs={"class": "form-control"}),
        }


class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
    )
    new_password2 = forms.CharField(
        label="New Password Confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]
