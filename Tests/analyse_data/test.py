import unittest
import pandas as pd
from flask import Flask
from flask_testing import TestCase
from datetime import date, timedelta
from decimal import Decimal

# This demands that we run from the Thalia directory.
# TODO: make it work no matter which directory it's run from.
import sys
import os

sys.path.insert(0, "./analyse_data")
from analyse_data import *


class TestTotalReturn(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    def setUp(self):
        self.start = date(2000, 1, 1)
        self.end = date(2000, 1, 20)
        self.dates = pd.date_range(self.start, self.end, freq=timedelta(days=1))
        gold_prices = [
            [
                Decimal("6.00") + i * Decimal("0.03"),
                Decimal("0.00"),
                Decimal("0.00"),
                Decimal("0.00"),
            ]
            for (i, _) in enumerate(self.dates)
        ]
        silver_prices = [
            [
                Decimal("1.00") + i * i * Decimal("0.01"),
                Decimal("0.00"),
                Decimal("0.00"),
                Decimal("0.00"),
            ]
            for (i, _) in enumerate(self.dates)
        ]
        rock_prices = [
            [Decimal("1.00"), Decimal("1.00"), Decimal("1.00"), Decimal("1.00"),]
            for _ in self.dates
        ]
        self.gold_data = pd.DataFrame(
            gold_prices, index=self.dates, columns=["Open", "Low", "High", "Close"]
        )
        self.silver_data = pd.DataFrame(
            silver_prices, index=self.dates, columns=["Open", "Low", "High", "Close"]
        )
        self.rock_data = pd.DataFrame(
            rock_prices, index=self.dates, columns=["Open", "Low", "High", "Close"]
        )

    def test_single_asset(self):
        starting_balance = Decimal("23.46")
        contribution_dates = set()
        contribution_amount = None
        rebalancing_dates = set()

        assets = [{"ticker": "GOLD", "weight": 1.0, "values": self.gold_data}]

        risk_free_rate = None

        strategy = Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
            risk_free_rate,
        )

        roi = total_return(strategy)
        self.assertEqual(roi.at[self.start], Decimal("23.46"))
        self.assertEqual(roi.at[date(2000, 1, 12)], Decimal("24.75"))
        self.assertEqual(roi.at[self.end], Decimal("25.69"))

    def test_contribution(self):
        starting_balance = Decimal("1.00")
        contribution_dates = self.dates
        contribution_amount = Decimal("1.00")
        rebalancing_dates = set()

        assets = [{"ticker": "ST", "weight": 1.0, "values": self.rock_data}]

        risk_free_rate = None

        strategy = Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
            risk_free_rate,
        )

        roi = total_return(strategy)
        self.assertEqual(Decimal("2.00"), roi.at[self.start])
        for (day, next_day) in zip(self.dates, self.dates[1:]):
            self.assertEqual(roi[day] + Decimal("1.00"), roi[next_day])


class TestSharpeRatio(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        return app

    def setUp(self):
        self.msft_vals = pd.read_csv(
            "file://"
            + os.path.dirname(os.path.realpath(__file__))
            + "/test_data/MSFT.csv",
            index_col="Date",
            converters={
                "Open": Decimal,
                "High": Decimal,
                "Low": Decimal,
                "Close": Decimal,
            },
        )
        self.risk_free_vals = pd.read_csv(
            "file://"
            + os.path.dirname(os.path.realpath(__file__))
            + "/test_data/risk_free_rate.csv",
            index_col="Date",
        )
        self.msft_vals.index = pd.to_datetime(self.msft_vals.index)
        self.risk_free_vals.index = pd.to_datetime(self.risk_free_vals.index)

    def test_sharpe_ratio(self):
        starting_balance = Decimal("10000")
        contribution_dates = set()
        contribution_amount = None
        rebalancing_dates = set()
        start_date = date(1986, 3, 13)
        end_date = date(2020, 1, 24)
        risk_free_vals = self.risk_free_vals

        self.msft_vals = self.msft_vals.reindex(
            pd.date_range(start_date, end_date)
        ).ffill()

        assets = [{"ticker": "MSFT", "weight": 1.0, "values": self.msft_vals}]

        strategy = Strategy(
            start_date,
            end_date,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
            Decimal(1.004388968),
        )
        print(sharpe_ratio(strategy))


if __name__ == "__main__":
    unittest.main()
