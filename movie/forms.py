from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from movie.models import Movies,RatingMovie,UserProfile

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","username","email","password1","password2"]

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user",)

class MovieForm(forms.ModelForm):
    class Meta:
        model=Movies
        fields="__all__"
        # exclude=("liked_by",)

class RatingMovieForm(forms.ModelForm):
    class Meta:
        model=RatingMovie
    
        fields=["movie","user","rating","comment"]
        widgets = {
            'rating': forms.Select(choices=RatingMovie.RATING_CHOICES),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }