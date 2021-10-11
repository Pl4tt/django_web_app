from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate

from .models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length="60", help_text="Email is required. Please enter a valid email address.")

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")
    
    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        try:
            Account.objects.get(email=email)
        except Exception as e:
            print(e)
            return email
        
        raise forms.ValidationError(f"Email '{email}' is already in use.")
    
    def clean_username(self):
        email = self.cleaned_data["username"]

        try:
            Account.objects.get(email=email)
        except Exception as e:
            print(e)
            return email
        
        raise forms.ValidationError(f"Email '{email}' is already in use.")


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"].lower()
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid email or password.")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("biography", "username", "email", "hide_email")

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.biography = self.cleaned_data["biography"]
        account.username = self.cleaned_data["username"]
        account.email = self.cleaned_data["email"].lower()
        account.hide_email = self.cleaned_data["hide_email"]

        if commit:
            account.save()
        return account
            
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        return forms.ValidationError("Username is already in use :(")
    
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        return forms.ValidationError("Email is already in use :((")