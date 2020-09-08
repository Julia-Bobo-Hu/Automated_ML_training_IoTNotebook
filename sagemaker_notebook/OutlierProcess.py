# ----------------------------------------------------------------------------
# File name: OutlierProcess.py
#
# Created on: Aug. 11 2020
#
#  by Julia Hu
#
# Description:
#
# 1) This module to remove abnormal reading for different meter types
#
#       
#
# -----------------------------------------------------------------------------
#first load in all necessary librares 
import pandas as pd
import numpy as np
import datetime
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder

class OutlierTransformer( BaseEstimator, TransformerMixin ):
    #Class constructor method that takes in a list of values as its argument
    def __init__(self, electric_outlier=True, chill_outlier=True, hot_outlier=True):
        self._electric_outlier = electric_outlier
        self._chill_outlier = chill_outlier
        self._hot_outlier = hot_outlier
        
    #Return self nothing else to do here
    def fit( self, X, y = None):
        return self
    
    #Transformer method we wrote for this transformer 
    def transform(self, X):
        funny_electric_bids = [803, 1088,  993, 799]
        funny_chill_bids = [778, 1088]
        funny_hot_bids = [1331,1021,794]
        
        if self._electric_outlier:
            for bid in funny_electric_bids:
                
                X = X [ ~((X['building_id'] == bid) & (X['meter'] == 0)) ]
        if self._chill_outlier:
            for bid in funny_chill_bids:
                
                X = X [ ~((X['building_id'] == bid) & (X['meter'] == 1)) ]
        if self._hot_outlier:
            for bid in funny_hot_bids:
                
                X = X [ ~((X['building_id'] == bid) & (X['meter'] == 3)) ]
        
        X = X.reset_index().drop('index',axis=1)
   
        return X