from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Adventure

# user registration for a new user.
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# a form for someone to contact the site administrator
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

# adventure form to create a new adventure
class AdventureForm(forms.ModelForm):
    class Meta:
        model = Adventure
        fields = ['picture', 'description', 'max_participants', 'location', 'tag', 'event_datetime', 'status']
        widgets = {
            'event_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
