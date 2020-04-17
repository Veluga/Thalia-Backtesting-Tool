from flask_login import current_user
from Thalia.extensions import db
from Thalia.models.portfolio import Portfolio
import pandas as pd

from analyse_data.analyse_data import Strategy, Asset


def store_portfolio(start_date, end_date, starting_balance, name, table):
    success = True
    strat = Strategy(start_date, end_date, starting_balance, [], [], None, [])

    strat.assets = [Asset(tkr, allocation, pd.DataFrame()) for tkr, allocation in table]

    if Portfolio.query.filter_by(name=name).scalar() is not None:
        success = False

    porto = Portfolio()
    porto.set_strategy(strat)
    porto.shared = False
    porto.name = name
    porto.owner = current_user.id

    db.session.add(porto)
    db.session.commit()

    return success


def retrieve_portfolio(portfolio_id):
    porto = Portfolio.query.get(portfolio_id)
    strat = porto.get_strategy()
    return porto, strat


def get_portfolios_list():
    portos = Portfolio.query.filter_by(owner=current_user.id).with_entities(
        Portfolio.id, Portfolio.name
    ).all()
    return portos
