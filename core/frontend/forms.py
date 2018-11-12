from django.forms import ModelForm, PasswordInput
from django import forms
from .models import temp_pers_keywords, temp_keywords, temp_main, Document, jra_settings


class SelectMain(ModelForm):
    class Meta:
        model = temp_main
        fields = ['descr']
        widgets = {
            'descr': forms.Select(
                attrs={'id': 'post-text', 'label': '', 'initial': '', 'required': True}
            ),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'dfolder', 'document')

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['description'].label = "Upload description"
        self.fields['dfolder'].label = "Folder path"
        self.fields['document'].label = "Single file path"

# ADMIN PANEL FORMS
# Create custom form with specific queryset for filter pers and standard keywords in select:
class CustomBarModelForm(ModelForm):
    class Meta:
        model = temp_pers_keywords
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomBarModelForm, self).__init__(*args, **kwargs)
        self.fields['pers_id'].queryset = temp_keywords.objects.filter(personal=1)
        self.fields['standard_id'].queryset = temp_keywords.objects.filter(personal=0)

        
class jra_settingsForm(ModelForm):
    j_pass = forms.CharField(widget=PasswordInput())
    class Meta:
        model = jra_settings
        labels = {
            "j_pass": "Password"
        }
        fields = '__all__'        
