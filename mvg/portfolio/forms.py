from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout, Button, Row, Column
from betterforms.multiform import MultiModelForm

""" We are using modelforms, that is our forms are connected to the database, and upo user input, a new entry is added.  """

PORTFOLIO_COUNTER = 0

class AssetForm(forms.Form):
    assetTicker = forms.CharField(max_length=256,required=False)
    percentage = forms.DecimalField(max_digits=50, decimal_places=20,required=False)

    """ Add form helper here """
    def __init__(self, *args, **kwargs):
        super(AssetForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'row'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            Row(
                Column('assetTicker', css_class='form-group col-md-6 mb-0'),
                Column('percentage', css_class='form-group col-md-6 mb-0'),
                css_class='form-row')
            )
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.form_tag = False
        self.helper.disable_csrf = True



