from django import forms
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

    #Check match password n confirm
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                " Password does match!"
            )