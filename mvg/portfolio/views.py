from django.shortcuts import render, redirect
from .forms import AssetForm
from django.views.generic import TemplateView
from django.urls import reverse
from . import keyFigures

""" Main input view """
class PortfolioView(TemplateView):
    template_name = "portfolio/form.html"

    """ GET request """
    def get(self,request):
        form = AssetForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    """ POST request """
    def post(self, request):
        return self.get(request)


""" Main output view """
class ResultsView(TemplateView):
    template_name = "portfolio/out.html"

    """ GET request """
    def get(self,request):
        args = {}
        return render(request, self.template_name, args)

    """ POST request """
    def post(self, request):
        form = AssetForm(request.POST)
        if form.is_valid():
            asset1 = form.cleaned_data["asset1"]
            percentage1 = form.cleaned_data["percentage1"]

            asset2 = form.cleaned_data["asset2"]
            percentage2 = form.cleaned_data["percentage2"]

            asset3 = form.cleaned_data["asset3"]
            percentage3 = form.cleaned_data["percentage3"]
            
            print (asset1,percentage1)
            print (asset2,percentage2)
            print (asset3,percentage3)


            """ Initialise portfolio as a portfolio object """
            """ Its attributes are printed in the form if named correctly """
            portfolio = 1  
            args = { "portfolio": portfolio }


        return render(request, self.template_name, args)


