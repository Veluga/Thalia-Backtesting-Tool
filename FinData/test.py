import pandas as pd


df = pd.DataFrame(
    [
        {"AssetClassName": "BEVERAGE"},
        {"AssetClassName": "FOOD"},
        {"AssetClassName": "MEDIA"},
    ]
)

df0 = pd.DataFrame(
    [
        {"AssetClassName": "FOOD", "AssetTicker": "ASS13", "Name": "AssetOne"},
        {"AssetClassName": "FOOD", "AssetTicker": "ASS2", "Name": "AssetTwo"},
        {"AssetClassName": "BEVERAGE", "AssetTicker": "ASS3", "Name": "AssetThree"},
    ]
)


df1 = pd.DataFrame(
    [
        {
            "AssetTicker": "ASS13",
            "ADate": "2020-02-01",
            "ALow": "1.0",
            "AHigh": "1",
            "AOpen": "1",
            "AClose": "1",
            "IsInterpolated": 1,
        },
        {
            "AssetTicker": "ASS13",
            "ADate": "2020-02-02",
            "ALow": "2.0",
            "AHigh": "2",
            "AOpen": "2",
            "AClose": "2",
            "IsInterpolated": 1,
        },
        {
            "AssetTicker": "ASS13",
            "ADate": "2020-02-03",
            "ALow": "3.0",
            "AHigh": "3",
            "AOpen": "3",
            "AClose": "3",
            "IsInterpolated": 0,
        },
    ]
)

df2 = pd.DataFrame(
    [
        {
            "AssetTicker": "ASS13",
            "ADate": "2020-02-05",
            "ALow": "1.0",
            "AHigh": "1",
            "AOpen": "1",
            "AClose": "1",
            "IsInterpolated": 1,
        },
        {
            "AssetTicker": "ASS13",
            "ADate": "2020-02-06",
            "ALow": "2.0",
            "AHigh": "2",
            "AOpen": "2",
            "AClose": "2",
            "IsInterpolated": 1,
        },
        {
            "AssetTicker": "ASS13",
            "ADate": "2020-02-04",
            "ALow": "3.0",
            "AHigh": "3",
            "AOpen": "3",
            "AClose": "3",
            "IsInterpolated": 0,
        },
    ]
)

df1 = df1.set_index(["AssetTicker", "ADate"])
df2 = df2.set_index(["AssetTicker", "ADate"])
import fd_manager as fdm

df = df.set_index("AssetClassName")

df0 = df0.set_index("AssetTicker")

fdm.FdMultiController.fd_create("testDB1")
conn = fdm.FdMultiController.fd_connect("testDB1", "rwd")
conn.write.write_asset_classes(df)
conn.write.write_assets(df0)
conn.write.write_asset_values(df1)
conn.write.write_asset_values(df2)
