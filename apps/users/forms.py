import re

from django import forms
from django.contrib.auth import get_user_model

from apps.users.models import UserProfile

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    Form with validations for user
    """

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with provided username already exists!")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with provided email already exists!")
        return email


class UserProfileCreationForm(forms.ModelForm):
    """
    Form with validations for user profile
    """

    class Meta:
        model = UserProfile
        fields = ["user", "name", "mobile_number", "bio", "date_of_birth"]

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data["mobile_number"]
        regular_exp = "[6-9][0-9]{9}"
        pattern = re.compile(regular_exp)
        if re.match(pattern, mobile_number) is None:
            raise forms.ValidationError("Please enter 10 digit mobile number!")
        return mobile_number
