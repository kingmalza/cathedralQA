from django.forms import ModelForm, PasswordInput
from django import forms
from .models import temp_pers_keywords, temp_keywords, Document, jra_settings, settings_gen, temp_main, temp_case, temp_variables, temp_library, temp_test_keywords, temp_pers_keywords


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
        help_texts = {'main_id': "Main template to which to connect the keyword",
                      'pers_id': 'Personal keyword connected to the template',
                      'standard_id': 'Standard keyword connected to the template',
                      'variable_val': 'Value for the keyword'}

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


class TempMainForm(forms.ModelForm):
    class Meta:
        model = temp_main
        fields = '__all__'
        help_texts = {'descr': "General description for the template",
                      'notes': 'The template notes will be displayed in the selection window on the test start screen'}


class TempCaseForm(forms.ModelForm):
    class Meta:
        model = temp_case
        fields = '__all__'
        help_texts = {'main_id': "Main template to which to connect the testcase",
                      'descr': 'The name of the test case that will be shown in the test structure'}


class TempVarsForm(forms.ModelForm):
    class Meta:
        model = temp_variables
        fields = '__all__'
        help_texts = {'main_id': "Main template to which to connect the variable Key/Val",
                      'v_key': 'Variable name',
                      'v_val': 'Optional, initial value shown on the test start screen'}


class TempLibsForm(forms.ModelForm):
    class Meta:
        model = temp_library
        fields = '__all__'
        help_texts = {'main_id': "Main template to which to connect the variable Key/Val",
                      'l_type': 'Type of library (Example Documentation, Library, Test Setup, etc.)',
                      'l_val': 'Value of the chosen library type',
                      'l_group': 'Grouping or not of library values'}


class TtkForm(forms.ModelForm):
    class Meta:
        model = temp_test_keywords
        fields = '__all__'
        help_texts = {'main_id': "Main template to which to connect the keyword",
                      'test_id': 'Main testcase to which to connect',
                      'key_id': 'Standard keyword connected to testcase',
                      'key_val': 'Value for the key',
                      'key_group': 'Grouping or not of keywords values'}
