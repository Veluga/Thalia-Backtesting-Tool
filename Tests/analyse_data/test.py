import unittest
import pandas as pd
from flask import Flask
from flask_testing import TestCase
from datetime import date
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

    def test(self):
        start = date(2000, 1, 1)
        end = date(2000, 1, 7)

        dates = pd.date_range(start=start, end=end, freq="D")

        starting_balance = Decimal("23.46")
        contribution_interval = None
        contribution_amount = None
        rebalancing_interval = None

        gold_prices = [
            [Decimal("1"), Decimal("0.0")],
            [Decimal("4"), Decimal("0.0")],
            [Decimal("9"), Decimal("0.0")],
            [Decimal("16"), Decimal("0.0")],
            [Decimal("25"), Decimal("0.0")],
            [Decimal("36"), Decimal("0.0")],
            [Decimal("49"), Decimal("0.0")],
        ]

        silver_prices = [
            [Decimal("0.5"), Decimal("0.6")],
            [Decimal("1.0"), Decimal("1.1")],
            [Decimal("1.5"), Decimal("1.6")],
            [Decimal("2.0"), Decimal("2.1")],
            [Decimal("2.5"), Decimal("2.6")],
            [Decimal("3.0"), Decimal("3.1")],
            [Decimal("3.5"), Decimal("3.6")],
        ]

        gold_data = pd.DataFrame(gold_prices, index=dates, columns=["Open", "Close"])
        silver_data = pd.DataFrame(
            silver_prices, index=dates, columns=["Open", "Close"]
        )

        assets = [
            {"ticker": "GOLD", "weight": 0.3, "values": gold_data},
            {"ticker": "SLV", "weight": 0.7, "values": silver_data},
        ]

        risk_free_rate = None

        strategy = Strategy(
            start,
            end,
            starting_balance,
            assets,
            contribution_interval,
            contribution_amount,
            rebalancing_interval,
            risk_free_rate,
        )

        print(total_return(strategy))


if __name__ == "__main__":
    unittest.main()
