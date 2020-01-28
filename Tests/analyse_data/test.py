import unittest
import pandas as pd
from flask import Flask
from flask_testing import TestCase
from datetime import date, timedelta
from decimal import Decimal

# This demands that we run from the Thalia directory.
# TODO: make it work no matter which directory it's run from.
import sys

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

    def test_rebalancing(self):
        # TODO
        starting_balance = Decimal("1.00")
        contribution_dates = set()
        contribution_amount = Decimal("0.0")
        rebalancing_dates = self.dates

        assets = None

    def test_mult_assets(self):
        starting_balance = Decimal("100.00")
        contribution_dates = set()
        contribution_amount = Decimal("0.0")
        rebalancing_dates = set()

        assets = [
            {"ticker": "GOLD", "weight": 0.4, "values": self.gold_data},
            {"ticker": "SLV", "weight": 0.6, "values": self.silver_data},
        ]

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
        print(f"\n{roi}\n")


if __name__ == "__main__":
    unittest.main()
