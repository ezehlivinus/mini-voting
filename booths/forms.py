from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', )

    
    # def clean(self):
    #     cleaned_data = super(CustomUserCreationForm,  self).clean()
        
    #     username = cleaned_data.get('username')

    #     if '/' not in username:
    #         raise forms.ValidationError('Error on username')

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if '/' not in username:
    #         raise forms.ValidationError('Error on username. The username is invalid')
        
    #     year, serail_number = username.split('/')

    #     if isinstance(int(year), int) is False and isinstance(int(serail_number), int) is False:
    #         raise forms.ValidationError('Error on username. The username is invalid')
    #     return username



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email', )


