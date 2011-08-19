from django.forms import ModelForm

import models

class CommuteForm(ModelForm):
    
    class Meta:
        
        model = models.Commute
        exclude = ('user')