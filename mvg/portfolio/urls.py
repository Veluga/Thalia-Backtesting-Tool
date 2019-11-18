from django.conf.urls import url
from . import views

app_name = "portfolio"

urlpatterns = [
    url(r'^$', views.PortfolioView.as_view(),name="input"),
    url(r'out/$', views.ResultsView.as_view(),name="output"),
]
