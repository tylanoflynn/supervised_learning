import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class TargetAverager(BaseEstimator, TransformerMixin):
    def __init__(self, group_by_feature, target_tendency = "mean"):
        self.ct_df = pd.DataFrame()
        self.group_by_feature = group_by_feature
        self.target_tendency = target_tendency
        self.ct = pd.Series()
    
    def get_central_tendencies(self, data, target_feature):
        self.ct_df = data.groupby(self.group_by_feature)[target_feature].describe()

    def set_central_tendency(self):
        self.ct = self.ct_df[self.target_tendency]
    
    def fit(self, X, y):
        Xtemp = X.merge(y, left_index = True, right_index = True)
        target_feature = Xtemp.columns[-1]
        self.get_central_tendencies(Xtemp, target_feature)
        self.set_central_tendency()
        return self

    def transform(self, X, y=None):
        X = X.merge(self.ct, left_on=self.group_by_feature, right_index=True, how='left')
        X = X.drop(labels=self.group_by_feature, axis=1)
        return X