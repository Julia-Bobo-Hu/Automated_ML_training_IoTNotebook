# ----------------------------------------------------------------------------
# File name: LabelEncode.py
#
# Created on: Aug. 11 2020
#
#  by Julia Hu
#
# Description:
#
# 1) This module to label encoding the primary use of each building
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

class CategoricalTransformer( BaseEstimator, TransformerMixin ):
    #Class constructor method that takes in a list of values as its argument
    def __init__(self):
        pass
        
    #Return self nothing else to do here
    def fit( self, X, y = None):
        return self
    
    #Transformer method we wrote for this transformer 
    def transform(self, X , y = None ):        
            # Encode Categorical Data
        le = LabelEncoder()
        X.loc[:,'primary_use'] = le.fit_transform(X["primary_use"])
   
        return X