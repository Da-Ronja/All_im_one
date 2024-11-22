from django import forms
from django.contrib.auth.models import User
from users.models import UserProfileInfo
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[validate_password]
        )

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e)
        return password


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')