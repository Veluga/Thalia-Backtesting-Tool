from Thalia.dashboard import user_csv

import pytest
import base64
import pandas as pd
import os
import time

from datetime import timedelta, date
from decimal import Decimal


def test_user_data():
    csv_data = (
        "Date,Open,High,Low,Close\n"
        "12-12-1980,0.51,0.50,0.51,0.51\n"
        "15-12-1980,0.48,0.48,0.48,0.48\n"
        "16-12-1980,0.45,0.45,0.45,0.45\n"
    )
    encoded = base64.b64encode(csv_data.encode("utf-8"))
    empty = os.listdir(user_csv.USER_DATA_DIR)
    handle = user_csv.store(encoded, timeout=timedelta(seconds=2))
    assert empty != os.listdir(user_csv.USER_DATA_DIR)
    retrieved = user_csv.retrieve(handle)
    expected = pd.DataFrame(
        [
            [Decimal("0.51"), Decimal("0.50"), Decimal("0.51"), Decimal("0.51")],
            [Decimal("0.51"), Decimal("0.50"), Decimal("0.51"), Decimal("0.51")],
            [Decimal("0.51"), Decimal("0.50"), Decimal("0.51"), Decimal("0.51")],
            [Decimal("0.48"), Decimal("0.48"), Decimal("0.48"), Decimal("0.48")],
            [Decimal("0.45"), Decimal("0.45"), Decimal("0.45"), Decimal("0.45")],
        ],
        columns=["Open", "High", "Low", "Close"],
        index=pd.date_range(date(1980, 12, 12), date(1980, 12, 16), freq="D"),
    )
    assert expected.equals(retrieved)
    time.sleep(4)
    assert empty == os.listdir(user_csv.USER_DATA_DIR)
