from analyse_data.analyse_data import Strategy
from ..extensions import db
import pickle

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strategy = db.Column(db.BLOB(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "<Portfolio {} {}>".format(self.id, len(self.strategy))

    def set_strategy(self, strat):
        self.strategy = pickle.dumps(strat)
    
    def get_strategy(self):
        return pickle.loads(self.strategy)