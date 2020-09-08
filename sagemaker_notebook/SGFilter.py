# ----------------------------------------------------------------------------
# File name: SGFilter.py
#
# Created on: Aug. 11 2020
#
#  by Julia Hu
#
# Description:
#
# 1) This module Smoothness filter for Time series data
#
#       
#
# -----------------------------------------------------------------------------
#first load in all necessary librares 
import pandas as pd
import numpy as np
import datetime
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.signal import savgol_filter as sg

class SGFilterTranformer(BaseEstimator, TransformerMixin):
    
    def __init__(self,SGFilter=True):
        self._SGFilter = SGFilter
    
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        w = 11
        p = 2
        if self._SGFilter:
            for si in X.site_id.unique():
                index = X.site_id == si
                X.loc[index, 'air_smooth'] = sg(X[index].air_temperature, w, p)
                X.loc[index, 'dew_smooth'] = sg(X[index].dew_temperature, w, p)
                X.loc[index, 'air_diff'] = sg(X[index].air_temperature, w, p, 1)
                X.loc[index, 'dew_diff'] = sg(X[index].dew_temperature, w, p, 1)
                X.loc[index, 'air_diff2'] = sg(X[index].air_temperature, w, p, 2)
                X.loc[index, 'dew_diff2'] = sg(X[index].dew_temperature, w, p, 2)
        return X