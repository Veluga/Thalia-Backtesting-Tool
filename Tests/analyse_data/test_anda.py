import unittest
import pandas as pd
import sys
import os
from flask import Flask
from flask_testing import TestCase
from datetime import date, timedelta
from decimal import Decimal

sys.path.insert(0, ".")
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
        starting_balance = Decimal("10000.00")
        contribution_dates = set()
        contribution_amount = Decimal("0.0")
        rebalancing_dates = self.dates

        assets = [
            anda.Asset("GOLD", Decimal("0.5"), self.gold_data),
            anda.Asset("SLV", Decimal("0.5"), self.silver_data),
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
        # print(roi)

    def test_no_money(self):
        starting_balance = Decimal("0.00")
        contribution_dates = pd.date_range(
            self.start, self.end, freq=timedelta(days=4)
        )[1:]
        contribution_amount = Decimal("1000.00")
        rebalancing_dates = set()

        assets = [anda.Asset("ST", Decimal("1.0"), self.rock_data)]

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
        # Just the lack of exception *should* be a sign of success.

    def test_mult_assets(self):
        starting_balance = Decimal("100.00")
        contribution_dates = set()
        contribution_amount = Decimal("0.0")
        rebalancing_dates = set()

        assets = [
            anda.Asset("GOLD", Decimal("0.4"), self.gold_data),
            anda.Asset("SLV", Decimal("0.6"), self.silver_data),
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
        self.assertEqual(roi[self.start + timedelta(days=14)], Decimal("220.40"))
        self.assertEqual(roi[self.end], Decimal("320.40"))


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
        self.berkshire_vals = pd.read_csv(
            "file://"
            + os.path.dirname(os.path.realpath(__file__))
            + "/test_data/BRK-A.csv",
            index_col="Date",
            converters={"Close": Decimal,},
        )
        self.risk_free_vals = pd.read_csv(
            "file://"
            + os.path.dirname(os.path.realpath(__file__))
            + "/test_data/risk_free_rate.csv",
            index_col="Date",
        )
        self.msft_vals.index = pd.to_datetime(self.msft_vals.index)
        self.berkshire_vals.index = pd.to_datetime(self.berkshire_vals.index)
        self.risk_free_vals.index = pd.to_datetime(self.risk_free_vals.index)

    def test_sharpe_ratio_single_asset(self):
        starting_balance = Decimal("10000")
        contribution_dates = set()
        contribution_amount = None
        rebalancing_dates = set()
        start_date = date(1986, 12, 31)
        end_date = date(2019, 12, 31)
        risk_free_vals = self.risk_free_vals

        self.msft_vals = self.msft_vals.reindex(
            pd.date_range(start_date, end_date)
        ).ffill()

        self.risk_free_vals = (
            self.risk_free_vals.dropna()["Close"]
            .reindex(pd.date_range(start_date, end_date))
            .ffill()
        )
        assets = [anda.Asset("MSFT", Decimal(1.0), self.msft_vals)]

        strategy = anda.Strategy(
            start_date,
            end_date,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
            self.risk_free_vals,
        )

        self.assertAlmostEqual(anda.sharpe_ratio(strategy), Decimal(0.74), delta=0.01)

    def test_sharpe_ratio_multi_asset(self):
        starting_balance = Decimal("10000")
        contribution_dates = set()
        contribution_amount = None
        rebalancing_dates = set()
        start_date = date(1989, 12, 29)
        end_date = date(2000, 12, 29)
        risk_free_vals = self.risk_free_vals

        self.msft_vals = self.msft_vals.reindex(
            pd.date_range(start_date, end_date)
        ).ffill()

        self.berkshire_vals = self.berkshire_vals.reindex(
            pd.date_range(start_date, end_date)
        ).ffill()

        self.risk_free_vals = (
            self.risk_free_vals.dropna()["Close"]
            .reindex(pd.date_range(start_date, end_date))
            .ffill()
        )
        assets = [
            anda.Asset("MSFT", Decimal(0.6), self.msft_vals),
            anda.Asset("BRK-A", Decimal(0.4), self.berkshire_vals),
        ]

        strategy = anda.Strategy(
            start_date,
            end_date,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
            self.risk_free_vals,
        )
        # self.assertAlmostEqual(anda.sharpe_ratio(strategy), Decimal(0.76), delta=0.01)


if __name__ == "__main__":
    unittest.main()
