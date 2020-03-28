import base64
import pandas as pd
import os
import time
import uuid
import multiprocessing

from datetime import timedelta, datetime
from decimal import Decimal

USER_DATA_DIR = os.path.join(os.path.dirname(__file__), "user-data/")
TIME_FMT = "%Y-%m-%d %H:%M:%S"


def store(encoded, timeout=timedelta(minutes=30)):
    """
    Takes the base64 representation of a user's custom uploaded data and
    stores it in a file. Returns a handle that can be passed to
    `retrieve` to get the data back.
    The data will only be valid for a short time (~30 minutes), so
    retrieval may fail.
    Raises a ValueError if the data is not valid utf-8. (maybe?)
    The caller should treat the handle as an opaque type, but if you
    need to modify this code it is a tuple of (str, datetime)
    representing the filepath ("user-data/<uuid>.csv") and last-accessible moment.
    Soon after the last-accessible moment, a subprocess will delete the
    file.
    The files are stored in the directory `Thalia/dashboard/user-data/`.
    """
    decoded_bytes = base64.b64decode(encoded)
    identifier = uuid.uuid4()
    filepath = os.path.join(USER_DATA_DIR, str(identifier) + ".csv")
    end_time = datetime.now() + timeout

    with open(filepath, "w") as out_file:
        out_file.write(decoded_bytes.decode("utf-8"))

    # We want a bit of buffer time to avoid race conditions.
    delay_sec = int(timeout.total_seconds() * 1.2)
    deleter = multiprocessing.Process(
        target=wait_and_delete, args=(filepath, delay_sec)
    )
    deleter.start()

    return (filepath, end_time.strftime(TIME_FMT))


def retrieve(handle):
    """
    Takes a handle returned by store and returns dataframe
    that can be passed to anda.
    If the file doesn't exist, or has timed out, raises FileNotFoundError.
    If the data is invalid, carries the exception upward from parser.
    """
    filepath, last_moment = handle

    last_moment = datetime.strptime(
        "".join(c for c in last_moment if c != "'"), TIME_FMT
    )

    if last_moment <= datetime.now():
        raise FileNotFoundError(f"{filepath} has timed out.")
    return parse_csv(filepath)


def wait_and_delete(filepath, delay_sec):
    # TODO: Security audit.
    assert USER_DATA_DIR == filepath[: len(USER_DATA_DIR)]
    assert ".." not in filepath
    assert "~" not in filepath
    assert "//" not in filepath
    time.sleep(delay_sec)
    try:
        os.remove(filepath)
    except Exception:
        pass


def parse_csv(data_file) -> pd.DataFrame:
    """
    Takes a csv file with columns [Date, Open, High, Low, Close] and returns
    a dataframe that can be put in an Asset object.
    If invalid, throws ValueError. (TODO)
    """
    df = pd.read_csv(
        data_file,
        index_col="Date",
        converters={
            "Open": Decimal,
            "High": Decimal,
            "Low": Decimal,
            "Close": Decimal,
        },
    )
    df.index = pd.to_datetime(df.index, format="%d-%m-%y")
    new_index = pd.date_range(df.index[0], df.index[-1], freq="D")
    df = df.reindex(new_index).ffill()
    return df