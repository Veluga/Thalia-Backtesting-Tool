from django.shortcuts import render, redirect
from .forms import AssetForm
from django.views.generic import TemplateView
from django.urls import reverse

""" Main input view """
class PortfolioView(TemplateView):
    template_name = "portfolio/form.html"

    """ GET request """
    def get(self,request):
        form1 = AssetForm()
        form2 = AssetForm()
        form3 = AssetForm()
        form4 = AssetForm()
        form5 = AssetForm()
        args = {'form1': form1, 'form2': form2,'form3': form3, 'form4': form4,'form5': form5}
        return render(request, self.template_name, args)

    """ POST request """
    def post(self, request):
        if request.method == "POST":
            form1 = AssetForm(request.POST)
            form2 = AssetForm(request.POST)
            form3 = AssetForm(request.POST)
            form4 = AssetForm(request.POST)
            form5 = AssetForm(request.POST)
            FORMS = [form1,form2,form3,form4,form5]

            for f in FORMS:
                if f.is_valid():
                    percentage = f.cleaned_data["percentage"]
                    category = f.cleaned_data["assetTicker"]
                    print (percentage,category)
                    print ()

            return self.get(request)

        else:
            print("\nHow would you even end up here?\n")
            # Somehow I did, then it magically stopped...
            return self.get(request)

