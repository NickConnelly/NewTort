from django import forms

from .models import Source

class SourceForm(forms.ModelForm):

    class Meta:
        model = Source
        fields = ('title', 'text','from_language','to_language','translation','alignment','frequency_list_exists',)
