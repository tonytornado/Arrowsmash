from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, HTML
from django import forms

from Scores.models import Score


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        # fields = {'song', 'score_rank', 'max_combo', 'marvelous', 'perfect', 'great', 'good', 'OK', 'miss', 'proof'}
        exclude = ('ex', 'player')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.layout = Layout(
                Row(
                    Column('song', css_class='form-group col-md-6 mb-0', type='date'),
                    Column('score_rank', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('marvelous', css_class='form-group col-md-2'),
                    Column('perfect', css_class='form-group col-md-2'),
                    Column('great', css_class='form-group col-md-2'),
                    Column('good', css_class='form-group col-md-2'),
                    Column('OK', css_class='form-group col-md-2'),
                    Column('miss', css_class='form-group col-md-2'),
                    css_class='form-row'
                ),
                Row(
                    Column(
                        HTML(
                            """{% if profile_form.proof.value %}
                            <img class="img-responsive img-thumbnail img-circle-avatar mr-auto" src={{ 
                            form.proof.value.url }}>
                            {% endif %}""", ), css_class='col-sm-6'),
                    Column('proof', css_class='col-sm-6 d-flex align-items-middle'),
                    css_class='col-sm-8 mx-auto py-4'
                ),
            )
