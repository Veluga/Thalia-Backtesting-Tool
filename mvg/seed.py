import csv
from datetime import datetime
from decimal import Decimal
from collections import namedtuple

from portfolio.models import AssetClass, Asset, Value

Datapoint = namedtuple('Datapoint', 'date open close lo hi')


def main():
    clear_tables()
    populate_asset_classes()
    populate_assets()
    populate_values()


def clear_tables():
    AssetClass.objects.all().delete()
    Asset.objects.all().delete()
    Value.objects.all().delete()


def populate_asset_classes():
    class_list = [
        'Equity', 'Fixed Income', 'Cryptocurrency', 'Commodity',
        'Foreign Exchange'
    ]

    for name in class_list:
        AssetClass(name=name).save()


def populate_assets():
    equities = AssetClass.objects.get(name='Equity').asset_set
    bonds = AssetClass.objects.get(name='Fixed Income').asset_set
    commodities = AssetClass.objects.get(name='Commodity').asset_set
    cryptocurrencies = AssetClass.objects.get(name='Cryptocurrency').asset_set

    equity_list = [
        ('Dow Jones', 'DOW'),
        ('S&P 500 Index', 'S&P500'),
        ('NASDAQ NMS Composite Index', 'NASDAQ'),
    ]

    bond_list = [
        ('Core US Aggregate Bond ETF', 'AGG'),
        ('Vanguard Total Bond Market', 'BND'),
        ('Investment Grate Corporate Bond', 'LQD'),
    ]

    commodity_list = [
        ('Shrimp', 'Shrimp'),
        ('Sugar', 'Sugar'),
        ('Tea', 'Tea'),
    ]

    cryptocurrency_list = [
        ('Bitcoin', 'BTC'),
        ('Etherium', 'ETH'),
        ('Ripple', 'XRP'),
    ]

    assets = [
        (equities, equity_list),
        (bonds, bond_list),
        (commodities, commodity_list),
        (cryptocurrencies, cryptocurrency_list),
    ]

    for asset in assets:
        fill_asset_set(asset[0], asset[1])


def fill_asset_set(asset_set, source_list):
        for item in source_list:
            asset_set.create(name=item[0], abbreviation=item[1])


def populate_values():
    populate_equity('DOW', '../Financial Data/Equities/Dow Jones.csv')

def populate_equity(ticker, filepath):
    print(f"Collecting {ticker} from {filepath}")
    equity_data = Asset.objects.get(abbreviation=ticker).value_set
    i = 0
    for datum in read_equity(filepath):
        equity_data.create(
            date=datum.date,
            open_price=datum.open,
            close_price=datum.close,
            low_price=datum.lo,
            high_price=datum.hi
        )

        if i % 500 == 0:
            print(f"{i} entries")
        i += 1

    print(f"Finished {ticker} with {i} entries")


def read_equity(filepath):
    with open(filepath) as src:
        reader = csv.reader(src, delimiter=',')
        next(reader)    # Ignore headings.
        for i, row in enumerate(reader):
            date = datetime.strptime(row[0], '%Y-%m-%d')
            open_price = Decimal(row[1])
            high_price = Decimal(row[2])
            low_price = Decimal(row[3])
            close_price = Decimal(row[4])

            yield Datapoint(
                date, open_price, close_price, low_price, high_price
            )


if __name__ == '__main__':
    main()
