from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class':'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password Again',
        'class':'form-control'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

        #U can add attrs here
        widgets = {
            'first_name':forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
            'last_name':forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
        }

    def __init__(self, *args, **kwargs):    #Here for overide all the fields u had
        super(RegistrationForm, self).__init__(*args, **kwargs)
        #U can add attrs here
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'

        #Loop through n add for all fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'