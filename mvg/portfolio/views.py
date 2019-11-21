from django.shortcuts import render, redirect
from .forms import AssetForm
from django.views.generic import TemplateView
from django.urls import reverse
from . import keyFigures
from . import userPortfolio
from plotly.offline import plot
from plotly.graph_objs import Scatter
import datetime
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
            #The following parameters are not provided by user
            #2019-09-30
            #2019-10-04
            startDate = datetime.datetime(day=1,month=9,year=2017)
            endDate = datetime.datetime(day=4,month=10,year=2019)
            initialVal = 100

            assets = {}
            if(percentage1 != '' and percentage1 != None ):
                assets[asset1]=percentage1
            if(percentage2 != '' and percentage2 != None ):
                assets[asset2]=percentage2
            if(percentage3 != '' and percentage3 != None ):
                assets[asset3]=percentage3

            print('#' * 100)
            print(assets)
            print('#' * 100)
            if(len(assets.keys()) == 0):
                assets['ERROR':0]
            porto = userPortfolio.Portfolio(assets)
            #print(porto.values(startDate, endDate))
            kfg = keyFigures.keyFigureGenerator(porto, startDate, endDate, initialVal)
            args = {
                'initial_balance':kfg.initialBalance,
                'end_balance':kfg.finalBalance,
                'best_year':kfg.bestYear,
                'worst_year':kfg.worstYear,
                'sortino_ratio':kfg.sortino,
                'sharpe_ratio':kfg.sharpe,
                'max_drawdown':kfg.maxDrawdown,
                }
            #args = { "portfolio": kfg}

            args = { "portfolio": porto, 'plot_div': plot_div}


        return render(request, self.template_name, args)
