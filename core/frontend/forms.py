from django.forms import ModelForm, PasswordInput
from django import forms
from .models import temp_pers_keywords, temp_keywords, temp_main, Document, jra_settings, settings_gen


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


class SettingsForm(forms.ModelForm):
    class Meta:
        model = settings_gen
        fields = ('tenant_name', 'stripe_id', 'paid_plan', 'comp_name', 'addr_1', 'addr_2', 'city',  'country','postal_zip', 'state_prov', 'tax_id', 'first_name', 'last_name',  'reg_email')
        help_texts = {'comp_name': "Unique identifier for the student", }

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        #self.fields['tenant_name'].label = "System Name"
        #self.fields['stripe_id'].label = "Account ID"
        #self.fields['paid_plan'].label = "Plan Type"
        self.fields['addr_1'].label = "Main Address"
        self.fields['addr_2'].label = "Secondary Address"
        self.fields['city'].label = "City"
        self.fields['comp_name'].label = "Company"
        self.fields['country'].label = "Country"
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['postal_zip'].label = "Zip Code"
        self.fields['state_prov'].label = "State/Province"
        self.fields['tax_id'].label = "Tax ID"
        self.fields['reg_email'].label = "Registered Email"