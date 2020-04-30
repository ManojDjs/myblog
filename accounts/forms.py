from django import forms
from django.contrib.auth.models import User
# from .models import Signup
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class userregistrationform(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    first_name = forms.CharField(max_length=200,
                                 widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

    # address=forms.Textarea()
    # address=forms.Textarea()
    # postcode=forms.Textarea()
    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.fields.TextInput(
                attrs={'placeholder': 'Enter your user name', 'class': 'form-control form-control-sm'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password', 'class': 'form-control form-control-sm'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Repeat password', 'class': 'form-control form-control-sm'})


class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ['image']


class userupdateform(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    first_name = forms.CharField(max_length=200,
                                 widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta():
        model = User
        fields = ['email', 'first_name', 'last_name']


class profileupdateform(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ['image']
        #
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['image'].widget.attrs.update(
        #         {'placeholder': 'Password', 'class': 'form-control form-control-sm'})
