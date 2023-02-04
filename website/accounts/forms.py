from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    email=forms.EmailField(max_length=64, help_text='Enter a valid email address')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        #fields = ('username', 'password1', 'password2', 'email', )

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args,
                                             **kwargs)
        for fieldname in ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
