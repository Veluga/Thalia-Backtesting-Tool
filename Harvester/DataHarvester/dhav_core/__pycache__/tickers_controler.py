import pandas as pd 

"""
    This will remain as it is until a later date when 
    free time is found in order to implement it.

    After-merge concern
"""

"""
    - There should be some way of removing dead tickers.
    - Checking the format of the tickers should be done by a method not visually 
    - Add further things that could be usefull when new assets will be added

    The methods below have been made very early in the development and they are
    hard coded. This should be changed into something more organized when time
    is available.
"""
class assetsControler():
    
    def show_all_tickers_hr(self):

        all_bonds = pd.read_csv("../tickers/bonds_tickers.csv")
        print(all_bonds)
        print("Data for bonds tickers: https://etfdb.com/etfs/bond/treasuries/")

        all_index_funds = pd.read_csv("../tickers/index_funds_tickers.csv")
        print(all_index_funds)
        print(
            "Data for index funds tickers: https://www.marketwatch.com/tools/mutual-fund/top25largest"
        )

        all_currency = pd.read_csv("../tickers/currency_tickers.csv")
        print(all_currency)
        print(
            "https://gist.github.com/Chintan7027/fc4708d8b5c8d1639a7c#file-currency-symbols-csv"
        )

        all_crypto = pd.read_csv("../tickers/crypto_tickers.csv")
        print(all_crypto)
        print("Those are the big ones at the time of making this: 31.1.2020")

        all_comodities = pd.read_csv("../tickers/comodities_future_tickers.csv")
        print(all_comodities)
        print("https://www.purefinancialacademy.com/futures-markets")


    def show_tickers_for(self, asset_class):

        if asset_class == "index_fund":
            all_index_funds = pd.read_csv("../tickers/index_funds_tickers.csv")
            print(all_index_funds)
            print(
                "Data for index funds tickers: https://www.marketwatch.com/tools/mutual-fund/top25largest"
            )
        elif asset_class == "bonds":
            all_bonds = pd.read_csv("../tickers/bonds_tickers.csv")
            print(all_bonds)
            print("Data for bonds tickers: https://etfdb.com/etfs/bond/treasuries/")

        elif asset_class == "currency":
            all_currency = pd.read_csv("../tickers/currency_tickers.csv")
            print(all_currency)
            print(
                "https://gist.github.com/Chintan7027/fc4708d8b5c8d1639a7c#file-currency-symbols-csv"
            )

        elif asset_class == "crypto":
            all_crypto = pd.read_csv("../tickers/crypto_tickers.csv")
            print(all_crypto)
            print("Those are the big ones at the time of making this: 31.1.2020")

        elif asset_class == "comodities_future":
            all_comodities = pd.read_csv("../tickers/comodities_future_tickers.csv")
            print(all_comodities)
            print("https://www.purefinancialacademy.com/futures-markets")
        else:
            print("asset_class_not_available")


    def get_tickers(self, asset_class):
        if asset_class == "bonds":
            return pd.read_csv("../tickers/bonds_tickers.csv")
        elif asset_class == "index_funds":
            return pd.read_csv("../tickers/index_funds_tickers.csv")
        elif asset_class == "currency":
            return pd.read_csv("../tickers/currency_tickers.csv")
        elif asset_class == "crypto":
            return pd.read_csv("../tickers/crypto_tickers.csv")
        elif asset_class == "comodities_future":
            return pd.read_csv("../tickers/comodities_future_tickers.csv")
        else:
            print("asset_class_unavailable")

