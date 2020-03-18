from analyse_data.analyse_data import Strategy
from ..extensions import db
import json
from datetime import datetime


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strategy = db.Column(db.JSON(), nullable=False)
    shared = db.Column(db.Boolean(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return "<Portfolio {} {}>".format(self.id, self.strategy)

    def set_strategy(self, strat):
        for asset in strat.assets:
            asset.values = None
            asset.dividends = None

        self.strategy = json.dumps(
            {
                "starting_balance": strat.starting_balance,
                "assets": strat.assets,
                "start_date": str(strat.dates[0]),
                "end_date": str(strat.dates[-1]),
            }
        )

    def get_strategy(self):
        stripped_strat = json.loads(self.strategy)

        return Strategy(
            datetime.strptime(stripped_strat["start_date"], "%Y-%m-%d %H:%M:%S"),
            datetime.strptime(stripped_strat["end_date"], "%Y-%m-%d %H:%M:%S"),
            stripped_strat["starting_balance"],
            [],
            [],
            None,
            [],
        )
