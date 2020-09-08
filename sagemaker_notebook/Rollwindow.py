# ----------------------------------------------------------------------------
# File name: Rollwindow.py
#
# Created on: Aug. 11 2020
#
#  by Julia Hu
#
# Description:
#
# 1) This module create rollowing window to find min, max, mean within following 24 hours
#
#       
#
# -----------------------------------------------------------------------------
#first load in all necessary librares 
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class RollwinTranformer(BaseEstimator, TransformerMixin):
    
    def __init__(self,Rollwin=True,window=3):
        self._Rollwin = Rollwin
        self._window = window
    
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        if self._Rollwin:
            group_df = X.groupby('site_id')
            cols = ['air_temperature', 'dew_temperature', 'precip_depth_1_hr', 'sea_level_pressure', 'wind_direction', 'wind_speed']
            rolled = group_df[cols].rolling(window=self._window, min_periods=0)
            lag_mean = rolled.mean().reset_index().astype(np.float16)
            lag_max = rolled.max().reset_index().astype(np.float16)
            lag_min = rolled.min().reset_index().astype(np.float16)
            lag_std = rolled.std().reset_index().astype(np.float16)
            for col in cols:
                X[f'{col}_mean_lag{self._window}'] = lag_mean[col]
                X[f'{col}_max_lag{self._window}'] = lag_max[col]
                X[f'{col}_min_lag{self._window}'] = lag_min[col]
                X[f'{col}_std_lag{self._window}'] = lag_std[col]
        return X