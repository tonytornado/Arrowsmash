from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Accounts.models import Profile


class SearchForm(forms.Form):
    searchstring = forms.CharField(max_length=50, label=False, required=False)

    def __init__(self, searchstring):
        super(SearchForm, self).__init__()
        self.fields['searchstring'].initial = searchstring
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('searchstring', css_class='form-control text-center', placeholder='Search (Press [Enter] to search)'),
        )


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
        exclude = ('user', 'bio')
        labels = {
            'rival_code': 'E-AMUSE Rival Code [Not Required, but encouraged!]',
        }
        help_texts = {
            'rival_code': 'XXXX-XXXX format, please',
            'avatar': 'Show your face, if you would. Nothing lewd, please.',
        }
        widgets = {
            'DOB': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('DOB', css_class='form-group col-md-6 mb-0', type='date'),
                Column('gender', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('rival_code', css_class='form-group col-md-6 mb-0'),
                Column('tagline', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('avatar', css_class='col-sm-6 mx-auto d-flex align-items-middle'),
                css_class='col-sm-8 mx-auto py-4'
            )
        )


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
                Column("city", css_class='form-group col-sm-10 mb-0'),
                Column('state', css_class='form-group col-sm-2 mb-0'),
                css_class='form-row'
            ),
            'bio',
            'gender',
            Row(
                Column(
                    HTML(
                        """{% if profile_form.avatar.value %}
                        <img class="img-responsive img-thumbnail img-circle-avatar mr-auto" src={{ profile_form.avatar.value.url }}>
                        {% endif %}""", ), css_class='col-sm-6'),
                Column('avatar', css_class='col-sm-6 d-flex align-items-middle'),
                css_class='col-sm-8 mx-auto py-4'
            )
        )
