from django import forms
from .models import Asset, Portfolio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout, Button
from betterforms.multiform import MultiModelForm

""" We are using modelforms, that is our forms are connected to the database, and upo user input, a new entry is added.  """

PORTFOLIO_COUNTER = 0

class AssetForm(forms.ModelForm):   
    class Meta:
        model = Asset
        fields = "__all__"

    """ Add form helper here """
    def __init__(self, *args, **kwargs):
        super(AssetForm,self).__init__(*args,**kwargs)    
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'   
        self.helper.form_class = 'form-inline'
        #self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.add_input(Submit('submit', 'Submit'))

        # This buttons shit
        self.helper.add_input(Button('NewPortfolio', "Add another portfolio", css_class='btn', onclick=self.createPortfolio()))

    # Only executes upon refresh needs to be checked
    def createPortfolio(self):
        global PORTFOLIO_COUNTER
        PORTFOLIO_COUNTER += 1
        newPortfolio = Portfolio(portfolioID=PORTFOLIO_COUNTER)
        newPortfolio.save()

