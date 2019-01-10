from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Accounts.models import Profile


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        labels = {
            'username': 'Desired Username',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'tagline', 'bio')
        labels = {
            'rival_code': 'E-AMUSE Rival Code [Not Required, but encouraged!]',
            'tagline': 'What would you say your life is like?',
        }
        help_texts = {
            'rival_code': 'XXXX-XXXX format, please',
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
        )


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'DOB')
        labels = {
            'rival_code': 'E-AMUSE Rival Code [Not Required, but encouraged!]',
            'tagline': 'What would you say your life is like?',
        }
        help_texts = {
            'rival_code': 'XXXX-XXXX format, please',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("tagline", css_class='form-group col-md-6 mb-0'),
                Column('rival_code', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column("city", css_class='form-group col-md-8 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'bio',
            'gender',
            Row(
                Column('avatar', css_class='form-group col-md-6 mx-auto'), css_class='form-row')
        )
