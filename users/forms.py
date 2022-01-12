from datetime import datetime as dt

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import DateInput

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('birthday',)
        widgets = {
            'birthday': DateInput(attrs={'type': 'date'}),
        }

    def clean_birthday(self, *args, **kwargs):
        birthday = self.cleaned_data.get('birthday')
        today = dt.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        if age < 14:
            raise forms.ValidationError('You must be at least 14 years old to sign up.')
        return birthday
        
        

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields