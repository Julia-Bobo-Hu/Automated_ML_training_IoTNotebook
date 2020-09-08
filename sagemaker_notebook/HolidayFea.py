# ----------------------------------------------------------------------------
# File name: HolidayFea.py
#
# Created on: Aug. 11 2020
#
#  by Julia Hu
#
# Description:
#
# 1) This module to ## Add holidays for different sites
#
#       
#
# -----------------------------------------------------------------------------
#first load in all necessary librares 
import pandas as pd
import numpy as np
import datetime
from sklearn.base import BaseEstimator, TransformerMixin
import holidays

en_holidays = holidays.England()
ir_holidays = holidays.Ireland()
ca_holidays = holidays.Canada()
us_holidays = holidays.UnitedStates()

class HolidayTranformer(BaseEstimator, TransformerMixin):
    
    def __init__(self,holiday=True):
        self._holiday = holiday
    
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        if self._holiday:
            en_idx = X.query('site_id == 1 or site_id == 5').index
            ir_idx = X.query('site_id == 12').index
            ca_idx = X.query('site_id == 7 or site_id == 11').index
            us_idx = X.query('site_id == 0 or site_id == 2 or site_id == 3 or site_id == 4 or site_id == 6 or site_id == 8 or site_id == 9 or site_id == 10 or site_id == 13 or site_id == 14 or site_id == 15').index
            
            X['IsHoliday'] = 0
            X.loc[en_idx, 'IsHoliday'] = X.loc[en_idx, 'timestamp'].apply(lambda x: en_holidays.get(x, default=0))
            X.loc[ir_idx, 'IsHoliday'] = X.loc[ir_idx, 'timestamp'].apply(lambda x: ir_holidays.get(x, default=0))
            X.loc[ca_idx, 'IsHoliday'] = X.loc[ca_idx, 'timestamp'].apply(lambda x: ca_holidays.get(x, default=0))
            X.loc[us_idx, 'IsHoliday'] = X.loc[us_idx, 'timestamp'].apply(lambda x: us_holidays.get(x, default=0))
            
            holiday_idx = X['IsHoliday'] != 0
            X.loc[holiday_idx, 'IsHoliday'] = 1
            X['IsHoliday'] = X['IsHoliday'].astype(np.uint8)
        
        X = X.drop(['timestamp'], axis = 1 )
    
        return X