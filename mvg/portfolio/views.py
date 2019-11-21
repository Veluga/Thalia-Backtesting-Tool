from django.shortcuts import render, redirect
from .forms import AssetForm
from django.views.generic import TemplateView
from django.urls import reverse
from . import keyFigures
from . import userPortfolio
from plotly.offline import plot
from plotly.graph_objs import Scatter
from datetime import date
from decimal import Decimal

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

            x_data = [0,1,2,3]
            y_data = [x**2 for x in x_data]
            plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')

            

            """ Initialise portfolio as a portfolio object """
            """ Its attributes are printed in the form if named correctly """
            porto = userPortfolio.Portfolio({'ass1': 0, 'ass2': 1, 'ass3': 0, 'ass4': 0, 'ass5': 0})
            kfg = keyFigures.keyFigureGenerator(porto,
                             date(day=1, month=10, year=2019),
                             date(day=29, month=10, year=2030),
                             Decimal('200'))
            
            print(porto.values(
                        date(day=1, month=10, year=2019),
                        date(day=5, month=10, year=2019)))

            args = { "portfolio": porto, 'plot_div': plot_div}


        return render(request, self.template_name, args)
