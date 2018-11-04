from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from clients.models import Client
class UserCreateForm(UserCreationForm):
    usertypes=[('client','Client'),('employee','Employee'),('user','User')]
    type = forms.CharField(required=True,widget=forms.Select(choices=usertypes))

    class Meta:
        model = User
        fields = ("username",  "password1", "password2","email")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data["type"]
        if commit:
            user.save()
        if user.first_name=="client":
            client = Client(name=self.cleaned_data['username'],client_id=user.id)
            client.save()
        return user