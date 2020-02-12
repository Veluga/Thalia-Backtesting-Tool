import unittest
import pandas as pd
import sys
import os

from unittest import TestCase
from datetime import date, timedelta
from decimal import Decimal

sys.path.insert(0, ".")
from analyse_data import analyse_data as anda

# TODO: these 3 have a lot of common code that can be DRY'd up.
def read_asset(path):
    asset_vals = pd.read_csv(
        "file://" + os.path.dirname(os.path.realpath(__file__)) + path,
        index_col="Date",
        converters={"Close": Decimal},
    )
    asset_vals.index = pd.to_datetime(asset_vals.index, format="%d/%m/%Y")
    return asset_vals


def read_risk_free():
    risk_free_vals = pd.read_csv(
        "file://"
        + os.path.dirname(os.path.realpath(__file__))
        + "/test_data/risk_free_rate.csv",
        index_col="Date",
    )
    risk_free_vals.index = pd.to_datetime(risk_free_vals.index, format="%d/%m/%Y")
    return risk_free_vals


def read_dividends(path):
    dividends = pd.read_csv(
        "file://"
        + os.path.dirname(os.path.realpath(__file__))
        + path,
        index_col="Date",
        converters={"Dividends": Decimal},
    )
    dividends.index = pd.to_datetime(dividends.index, format="%Y-%m-%d")
    return dividends


class TestTotalReturn(TestCase):
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
            [Decimal("1.00"), Decimal("1.00"), Decimal("1.00"), Decimal("1.00")]
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

        strategy = anda.Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
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

        assets = [anda.Asset("ST", Decimal("1.00"), self.rock_data)]

        strategy = anda.Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
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

        strategy = anda.Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
        )

        roi = anda.total_return(strategy)
        roi  # gotta keep flake8 happy.

    def test_no_money(self):
        starting_balance = Decimal("0.00")
        contribution_dates = pd.date_range(
            self.start, self.end, freq=timedelta(days=4)
        )[1:]
        contribution_amount = Decimal("1000.00")
        rebalancing_dates = set()

        assets = [anda.Asset("ST", Decimal("1.0"), self.rock_data)]

        strategy = anda.Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
        )

        roi = anda.total_return(strategy)
        roi  # Just the lack of exception *should* be a sign of success.

    def test_mult_assets(self):
        starting_balance = Decimal("100.00")
        contribution_dates = set()
        contribution_amount = Decimal("0.0")
        rebalancing_dates = set()

        assets = [
            anda.Asset("GOLD", Decimal("0.4"), self.gold_data),
            anda.Asset("SLV", Decimal("0.6"), self.silver_data),
        ]

        strategy = anda.Strategy(
            self.start,
            self.end,
            starting_balance,
            assets,
            contribution_dates,
            contribution_amount,
            rebalancing_dates,
        )

        roi = anda.total_return(strategy)
        self.assertEqual(roi[self.start], Decimal("100.00"))
        self.assertEqual(roi[self.start + timedelta(days=14)], Decimal("220.40"))
        self.assertEqual(roi[self.end], Decimal("320.40"))


class TestSharpeRatio(TestCase):
    def setUp(self):
        self.starting_balance = Decimal("10000")
        self.contribution_dates = set()
        self.contribution_amount = None
        self.rebalancing_dates = set()

        self.msft_vals = read_asset("/test_data/MSFT.csv")
        self.berkshire_vals = read_asset("/test_data/BRK-A.csv")
        self.risk_free_vals = read_risk_free()

    def test_sharpe_ratio_single_asset(self):
        start_date = date(1986, 12, 31)
        end_date = date(2019, 12, 31)

        msft_vals = self.msft_vals.reindex(pd.date_range(start_date, end_date)).ffill()
        risk_free_vals = (
            self.risk_free_vals.dropna()["Close"]
            .reindex(pd.date_range(start_date, end_date))
            .ffill()
        )

        assets = [anda.Asset("MSFT", Decimal("1.00"), msft_vals)]

        strategy = anda.Strategy(
            start_date,
            end_date,
            self.starting_balance,
            assets,
            self.contribution_dates,
            self.contribution_amount,
            self.rebalancing_dates,
        )

        self.assertAlmostEqual(
            anda.sharpe_ratio(strategy, risk_free_vals), Decimal(0.75), delta=0.05
        )

    def test_sharpe_ratio_multi_asset(self):
        start_date = date(1989, 12, 29)
        end_date = date(2000, 12, 29)

        msft_vals = self.msft_vals.reindex(pd.date_range(start_date, end_date)).ffill()
        berkshire_vals = self.berkshire_vals.reindex(
            pd.date_range(start_date, end_date)
        ).ffill()
        risk_free_vals = (
            self.risk_free_vals.dropna()["Close"]
            .reindex(pd.date_range(start_date, end_date))
            .ffill()
        )

        assets = [
            anda.Asset("MSFT", Decimal(0.6), msft_vals),
            anda.Asset("BRK-A", Decimal(0.4), berkshire_vals),
        ]

        strategy = anda.Strategy(
            start_date,
            end_date,
            self.starting_balance,
            assets,
            self.contribution_dates,
            self.contribution_amount,
            self.rebalancing_dates,
        )
        self.assertAlmostEqual(
            anda.sharpe_ratio(strategy, risk_free_vals), Decimal("0.89"), delta=0.2
        )


class TestMaxDrawdown(TestCase):
    def setUp(self):
        self.starting_balance = Decimal("10000")
        self.contribution_dates = set()
        self.contribution_amount = None
        self.rebalancing_dates = set()

        self.msft_vals = read_asset("/test_data/MSFT.csv")
        self.berkshire_vals = read_asset("/test_data/BRK-A.csv")
        self.risk_free_vals = read_risk_free()

    def test_max_drawdown_single_asset(self):
        start_date = date(1986, 12, 31)
        end_date = date(2019, 12, 31)

        msft_vals = self.msft_vals.reindex(pd.date_range(start_date, end_date)).ffill()

        assets = [anda.Asset("MSFT", Decimal("1.0"), msft_vals)]

        strategy = anda.Strategy(
            start_date,
            end_date,
            self.starting_balance,
            assets,
            self.contribution_dates,
            self.contribution_amount,
            self.rebalancing_dates,
        )
        self.assertAlmostEqual(anda.max_drawdown(strategy), Decimal("72.33"), delta=2.5)

    def test_max_drawdown_multi_asset(self):
        start_date = date(1989, 12, 29)
        end_date = date(2000, 12, 29)

        msft_vals = self.msft_vals.reindex(pd.date_range(start_date, end_date)).ffill()
        berkshire_vals = self.berkshire_vals.reindex(
            pd.date_range(start_date, end_date)
        ).ffill()

        assets = [
            anda.Asset("MSFT", Decimal(0.6), msft_vals),
            anda.Asset("BRK-A", Decimal(0.4), berkshire_vals),
        ]

        strategy = anda.Strategy(
            start_date,
            end_date,
            self.starting_balance,
            assets,
            self.contribution_dates,
            self.contribution_amount,
            self.rebalancing_dates,
        )
        self.assertAlmostEqual(anda.max_drawdown(strategy), Decimal("59.03"), delta=3)


class TestSortinoRatio(TestCase):
    def setUp(self):
        self.starting_balance = Decimal("10000")
        self.contribution_dates = set()
        self.contribution_amount = None
        self.rebalancing_dates = set()

        self.msft_vals = read_asset("/test_data/MSFT.csv")
        self.berkshire_vals = read_asset("/test_data/BRK-A.csv")
        self.risk_free_vals = read_risk_free()

    def test_sortino_ratio_single_asset(self):
        start_date = date(1986, 12, 31)
        end_date = date(2019, 12, 31)

        msft_vals = self.msft_vals.reindex(pd.date_range(start_date, end_date)).ffill()
        risk_free_vals = (
            self.risk_free_vals.dropna()["Close"]
            .reindex(pd.date_range(start_date, end_date))
            .ffill()
        )

        assets = [anda.Asset("MSFT", Decimal(1.0), msft_vals)]

        strategy = anda.Strategy(
            start_date,
            end_date,
            self.starting_balance,
            assets,
            self.contribution_dates,
            self.contribution_amount,
            self.rebalancing_dates,
        )
        self.assertAlmostEqual(
            anda.sortino_ratio(strategy, risk_free_vals), Decimal("1.34"), delta=0.1
        )

    def test_sortino_ratio_multi_asset(self):
        start_date = date(1989, 12, 29)
        end_date = date(2000, 12, 29)

        msft_vals = self.msft_vals.reindex(pd.date_range(start_date, end_date)).ffill()
        berkshire_vals = self.berkshire_vals.reindex(
            pd.date_range(start_date, end_date)
        ).ffill()
        risk_free_vals = (
            self.risk_free_vals.dropna()["Close"]
            .reindex(pd.date_range(start_date, end_date))
            .ffill()
        )

        assets = [
            anda.Asset("MSFT", Decimal(0.6), msft_vals),
            anda.Asset("BRK-A", Decimal(0.4), berkshire_vals),
        ]

        strategy = anda.Strategy(
            start_date,
            end_date,
            self.starting_balance,
            assets,
            self.contribution_dates,
            self.contribution_amount,
            self.rebalancing_dates,
        )
        self.assertAlmostEqual(
            anda.sortino_ratio(strategy, risk_free_vals), Decimal("1.56"), delta=0.2
        )


class TestBestWorstYear(TestCase):
    def setUp(self):
        self.starting_balance = Decimal("10000")
        self.contribution_dates = set()
        self.contribution_amount = None
        self.rebalancing_dates = set()

        self.msft_vals = read_asset("/test_data/MSFT.csv")
        self.berkshire_vals = read_asset("/test_data/BRK-A.csv")
        self.risk_free_vals = read_risk_free()

    def test_simple(self):
        start_date = date(1989, 1, 4)
        end_date = date(2010, 1, 1)

        self.msft_vals = self.msft_vals.reindex(
            pd.date_range(start_date, end_date)
        ).ffill()
        self.risk_free_vals = (
            self.risk_free_vals.dropna()["Close"]
            .reindex(pd.date_range(start_date, end_date))
            .ffill()
        )

        assets = [
            anda.Asset("MSFT", Decimal("1.0"), self.msft_vals),
        ]

        strategy = anda.Strategy(
            start_date,
            end_date,
            self.starting_balance,
            assets,
            self.contribution_dates,
            self.contribution_amount,
            self.rebalancing_dates,
        )

        b = anda.best_year(strategy)
        w = anda.worst_year(strategy)

        self.assertAlmostEqual(b, Decimal("120"), delta=2)
        self.assertAlmostEqual(w, Decimal("-63"), delta=2)


class TestDividends(TestCase):
    def setUp(self):
        self.starting_balance = Decimal("10000")
        self.contribution_dates = set()
        self.contribution_amount = None
        self.rebalancing_dates = set()

        self.msft_vals = read_asset("/test_data/MSFT.csv")
        self.msft_dividends = read_dividends("/test_data/MSFT_dividends.csv")
        self.aapl_vals = read_asset("/test_data/AAPL.csv")
        self.aapl_dividends = read_dividends("/test_data/AAPL_dividends.csv")

    def test_dividends_single_asset(self):
        start_date = date(1986, 12, 31)
        end_date = date(2019, 12, 31)

        msft_vals = self.msft_vals.reindex(pd.date_range(start_date, end_date)).ffill()
        msft_dividends = self.msft_dividends.reindex(
            pd.date_range(start_date, end_date)
        ).dropna()

        assets = [anda.Asset("MSFT", Decimal("1.0"), msft_vals, msft_dividends)]

        strategy = anda.Strategy(
            start_date,
            end_date,
            self.starting_balance,
            assets,
            self.contribution_dates,
            self.contribution_amount,
            self.rebalancing_dates,
        )
        self.assertAlmostEqual(
            anda.total_return(strategy)[end_date], Decimal("14599199.22"), delta=1
        )

    def test_dividends_multiple_assets(self):
        start_date = date(1986, 12, 31)
        end_date = date(2019, 12, 31)

        msft_vals = self.msft_vals.reindex(pd.date_range(start_date, end_date)).ffill()
        msft_dividends = self.msft_dividends.reindex(
            pd.date_range(start_date, end_date)
        ).dropna()
        aapl_vals = self.aapl_vals.reindex(pd.date_range(start_date, end_date)).ffill()
        aapl_dividends = self.aapl_dividends.reindex(
            pd.date_range(start_date, end_date)
        ).dropna()

        assets = [
            anda.Asset("MSFT", Decimal("0.5"), msft_vals, msft_dividends),
            anda.Asset("AAPL", Decimal("0.5"), aapl_vals, aapl_dividends),
        ]

        strategy = anda.Strategy(
            start_date,
            end_date,
            self.starting_balance,
            assets,
            self.contribution_dates,
            self.contribution_amount,
            self.rebalancing_dates,
        )
        self.assertAlmostEqual(
            anda.total_return(strategy)[end_date], Decimal("9856511.60"), delta=1
        )


if __name__ == "__main__":
    unittest.main()
