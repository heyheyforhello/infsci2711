from django import forms

from .models import Profile, Home, Business
from simplestore.checkout.models.address import Address


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.widgets.EmailInput)

    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password confirmation",
    )

    class Meta:
        model = Profile
        fields = ['first_name','last_name', 'email', 'password', 'password2', 'phone', 'kind',]

    def clean(self):
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data

    # def save(self, commit=True):
    #     profile = super(RegistrationForm, self).save(commit=False)
    #     profile.set_password(self.cleaned_data['password1'])
    #     if commit:
    #         profile.save()
    #     return profile

class PersonalAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['aid',]


class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        exclude = ['cid',]


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ['cid',]

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.widgets.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    class Meta:
        fields = ['email', 'password']
