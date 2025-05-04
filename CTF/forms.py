from django.contrib.auth.forms import UserCreationForm
from .models import CustomeUser
from django import forms


class UserReigstration(UserCreationForm):
    class Meta:
        model = CustomeUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")


    
