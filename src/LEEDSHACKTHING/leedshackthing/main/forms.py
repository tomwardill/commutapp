from django.forms import ModelForm, HiddenInput, CheckboxSelectMultiple

import models

class CommuteForm(ModelForm):
    
    class Meta:
        
        model = models.Commute
        exclude = ('user')
        widgets = {
            'box': HiddenInput(),
            'day_choices': CheckboxSelectMultiple(),
        }
        
    def __init__(self, *args, **kwargs):
        super(CommuteForm, self).__init__(*args, **kwargs)
    
        # Remove the 'hold ctrl' text, we don't need it, we're using a checkbox select
        self.fields['day_choices'].help_text = ''
