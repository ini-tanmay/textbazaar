from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from .models import User

# class NewUserForm(UserCreationForm):
# email = forms.EmailField(max_length=100, required=True)
# class Meta:
#     model = User
#     fields = ('username','company_email','first_name', 'email', 'designation','password1','password2')