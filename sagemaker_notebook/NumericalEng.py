# ----------------------------------------------------------------------------
# File name: NumericalEng.py
#
# Created on: Aug. 11 2020
#
#  by Julia Hu
#
# Description:
#
# 1) This module to engineer numerical features
#
#       
#
# -----------------------------------------------------------------------------
#first load in all necessary librares 
import pandas as pd
import numpy as np
import datetime
from sklearn.base import BaseEstimator, TransformerMixin
#Custom transformer we wrote to engineer features ( bathrooms per bedroom and/or how old the house is in 2019  ) 
#passed as boolen arguements to its constructor
class NumericalTransformer(BaseEstimator, TransformerMixin):
    #Class Constructor
    def __init__( self, outlier_1099=True,site0_corr=True, zone_corr=True, floor_cal=True, square_log=True,time_process=True, years_old=True):
        self._outlier_1099 = outlier_1099
        self._site0_corr = site0_corr
        self._zone_corr = zone_corr
        self._floor_cal = floor_cal
        self._square_log = square_log
        self._time_process = time_process
        self._years_old = years_old
        
    #Return self, nothing else to do here
    def fit( self, X, y = None ):
        return self 
    
    #Custom transform method we wrote that creates aformentioned features and drops redundant ones 
    def transform(self, X, y = None):
        #Check if needed 
        if self._outlier_1099:
            # Remove outliers
            X = X [ ~(X['building_id'] == 1099) ]
        if self._site0_corr:    
            #X = X.query('not (building_id <= 104 & meter == 0 & timestamp <= "2016-05-20")')
            X = X[~((X['building_id']<=104) & (X['meter']==0) & (X['timestamp'] <= "2016-05-20"))]
            
        X.loc[:,'timestamp'] =  pd.to_datetime(X['timestamp'])
        
        if self._zone_corr:
            zone_dict={0:4,1:0,2:7,3:4,4:7,5:0,6:4,7:4,8:4,9:5,10:7,11:4,12:0,13:5,14:4,15:4} 
            for sid, zone in zone_dict.items():
                sids = X.site_id == sid
                
                X.loc[sids,'timestamp'] = X.loc[sids,'timestamp']-pd.offsets.Hour(int(zone))
        
        if self._floor_cal:
            X.loc[:,'floor_area'] = X.square_feet / X.floor_count
            
        if self._square_log: 
            X.loc[:,'square_feet'] =  np.log1p(X['square_feet'])
        
        if self._time_process:
            # Add more features
            X.loc[:,"timestamp"] = pd.to_datetime(X.loc[:,"timestamp"],format="%Y-%m-%d %H:%M:%S")
            X.loc[:,"hour"] = X["timestamp"].dt.hour
            X.loc[:,"weekend"] = X["timestamp"].dt.weekday
            X.loc[:,"week"] = X["timestamp"].dt.week
            X.loc[:,"month"] = X["timestamp"].dt.month    
            
        #Check if needed     
        if self._years_old:
            #create new column
            X.loc[:,'yr_built'] =  2020 - X['year_built']

         
        # Sort by timestamp
        X.sort_values("timestamp", inplace=True)
        X.reset_index(drop=True, inplace=True)
        X = X.drop(["floor_count",'year_built'], axis = 1 )
    
        #returns a numpy array
        return X