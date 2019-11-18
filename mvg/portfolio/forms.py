from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout, Button, Row, Column
from betterforms.multiform import MultiModelForm
from . import assetclasses

""" We are using modelforms, that is our forms are connected to the database, and upo user input, a new entry is added.  """

PORTFOLIO_COUNTER = 0

class AssetForm(forms.Form):
    asset1 = forms.ChoiceField(required=False,choices=assetclasses.EQUITIES)
    percentage1 = forms.DecimalField(max_digits=50, decimal_places=20,required=False)

    asset2 = forms.ChoiceField(required=False,choices=assetclasses.EQUITIES)
    percentage2 = forms.DecimalField(max_digits=50, decimal_places=20,required=False)

    asset3 = forms.ChoiceField(required=False,choices=assetclasses.EQUITIES)
    percentage3 = forms.DecimalField(max_digits=50, decimal_places=20,required=False)

    """ Add form helper here """
    def __init__(self, *args, **kwargs):
        super(AssetForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'row'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            Row(
                Column('asset1', css_class='form-group col-md-6 mb-0'),
                Column('percentage1', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            Row(
                Column('asset2', css_class='form-group col-md-6 mb-0'),
                Column('percentage2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'),
            Row(
                Column('asset3', css_class='form-group col-md-6 mb-0'),
                Column('percentage3', css_class='form-group col-md-6 mb-0'),
                css_class='form-row')
            )
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.form_tag = False
        self.helper.disable_csrf = True



