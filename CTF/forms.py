from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomeUser
from django import forms


class UserRegistration(UserCreationForm):
    class Meta:
        model = CustomeUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistration, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'id' : 'username',
            'placeholder': 'Enter username',
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'id' : 'email',
            'placeholder': 'Enter email',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'id' : 'password1',
            'placeholder': 'Enter password',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'id' : 'password2',
            'placeholder': 'Confirm password',
            'class': 'form-control'
        })

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")


    
class UserLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'id' : 'username',
            'placeholder': 'Enter username',
            'class': 'form-control'
        })
        self.fields['password'].widget.attrs.update({
            'id' : 'password',
            'placeholder': 'Enter password',
            'class': 'form-control'
        })


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomeUser
        fields = ['profile_image']


class UpdateUsernameEmailForm(forms.ModelForm):
    class Meta:
        model = CustomeUser
        fields = ['username', 'email', 'bio']


