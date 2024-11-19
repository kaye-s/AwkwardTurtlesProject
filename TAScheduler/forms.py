
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Supervisor, User

class SupervisorAdminForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['user', 'admin_dept']  # Only fields belonging to Supervisor

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'fname', 'lname', 'phone_number', 'address']

    #UNNECESARY?
    # def clean_password1(self):
    #     password1 = self.cleaned_data.get("password1")
    #     try:
    #         validate_password(password1)
    #     except ValidationError as e:
    #         raise forms.ValidationError(e)
    #     return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user