import unittest
import pandas as pd
from flask import Flask
from flask_testing import TestCase
from datetime import date, timedelta
from decimal import Decimal

from analyse_data import analyse_data as anda


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
                Decimal("0.00"),
                Decimal("0.00"),
                Decimal("0.00"),
                Decimal("6.00") + i * Decimal("0.03"),
            ]
            for (i, _) in enumerate(self.dates)
        ]
        silver_prices = [
            [
                Decimal("0.00"),
                Decimal("0.00"),
                Decimal("0.00"),
                Decimal("1.00") + i * i * Decimal("0.01"),
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

        assets = [anda.Asset("Gold", Decimal("1.0"), self.gold_data)]

        risk_free_rate = None

        strategy = anda.Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
            risk_free_rate,
        )

        roi = anda.total_return(strategy)
        self.assertEqual(roi.at[self.start], Decimal("23.46"))
        self.assertEqual(roi.at[date(2000, 1, 12)], Decimal("24.75"))
        self.assertEqual(roi.at[self.end], Decimal("25.69"))

    def test_contribution(self):
        starting_balance = Decimal("1.00")
        contribution_dates = self.dates
        contribution_amount = Decimal("1.00")
        rebalancing_dates = set()

        assets = [anda.Asset("ST", Decimal(1.0), self.rock_data)]

        risk_free_rate = None

        strategy = anda.Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
            risk_free_rate,
        )

        roi = anda.total_return(strategy)
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
            anda.Asset("GOLD", Decimal("0.4"), self.gold_data),
            anda.Asset("SLV", Decimal("0.6"), self.gold_data),
        ]

        risk_free_rate = None

        strategy = anda.Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
            risk_free_rate,
        )

        roi = anda.total_return(strategy)
        self.assertEqual(roi[self.start], Decimal("100.00"))
        self.assertEqual(roi[date(2000, 1, 9)], Decimal("104.00"))
        self.assertEqual(roi[self.end], Decimal("109.50"))


if __name__ == "__main__":
    unittest.main()
