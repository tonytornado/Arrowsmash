from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from Scores.models import Score


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        exclude = ('player', 'date',)
        help_texts = {
            'proof': "We need you to show off your swag, mate.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Row(
                Column('marvelous', css_class='form-group col-md-2'),
                Column('perfect', css_class='form-group col-md-2'),
                Column('great', css_class='form-group col-md-2'),
                Column('good', css_class='form-group col-md-2'),
                Column('OK', css_class='form-group col-md-2'),
                Column('miss', css_class='form-group col-md-2'),
            ),
            'song',
            'proof',
            Submit('Submit', 'Submit', css_class='btn btn-block btn-outline-light'),
        )
