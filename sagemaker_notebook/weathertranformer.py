# ----------------------------------------------------------------------------
# File name: weathertranformer.py
#
# Created on: Aug. 11 2020
#
#  by Julia Hu
#
# Description:
#
# 1) This module contains function to feature engineering weatherdata
#
#       
#
# -----------------------------------------------------------------------------
#first load in all necessary librares 
import pandas as pd
import numpy as np
import datetime
from sklearn.base import BaseEstimator, TransformerMixin

class WeatherTranformer(BaseEstimator, TransformerMixin):
    
    def __init__(self,weather_fillna=True):
        self._weather_fillna = weather_fillna
    
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        if self._weather_fillna:
            # Find Missing Dates
            time_format = "%Y-%m-%d %H:%M:%S" 
            start_date = datetime.datetime.strptime(X['timestamp'].min(),time_format)
            end_date = datetime.datetime.strptime(X['timestamp'].max(),time_format)
            total_hours = int(((end_date - start_date).total_seconds() + 3600) / 3600)
            hours_list = [(end_date - datetime.timedelta(hours=x)).strftime(time_format) for x in range(total_hours)]
            
            missing_hours = []
            for site_id in X.site_id.unique():
                site_hours = np.array(X[X['site_id'] == site_id]['timestamp'])
                new_rows = pd.DataFrame(np.setdiff1d(hours_list,site_hours),columns=['timestamp'])
                new_rows['site_id'] = site_id
                X = pd.concat([X,new_rows])
                X = X.reset_index(drop=True) 
                
            # Add new Features
            X["datetime"] = pd.to_datetime(X["timestamp"])
            X["day"] = X["datetime"].dt.day
            X["week"] = X["datetime"].dt.week
            X["month"] = X["datetime"].dt.month    
            
            # Reset Index for Fast Update
            X = X.set_index(['site_id','day','month'])
            
            air_temperature_filler = pd.DataFrame(X.groupby(['site_id','day','month'])['air_temperature'].mean(),columns=["air_temperature"])
            X.update(air_temperature_filler,overwrite=False)
            
            # Step 1
            cloud_coverage_filler = X.groupby(['site_id','day','month'])['cloud_coverage'].mean()
            # Step 2
            cloud_coverage_filler = pd.DataFrame(cloud_coverage_filler.fillna(method='ffill'),columns=["cloud_coverage"])
            
            X.update(cloud_coverage_filler,overwrite=False)
            
            due_temperature_filler = pd.DataFrame(X.groupby(['site_id','day','month'])['dew_temperature'].mean(),columns=["dew_temperature"])
            X.update(due_temperature_filler,overwrite=False)
            
            # Step 1
            sea_level_filler = X.groupby(['site_id','day','month'])['sea_level_pressure'].mean()
            # Step 2
            sea_level_filler = pd.DataFrame(sea_level_filler.fillna(method='ffill'),columns=['sea_level_pressure'])
            X.update(sea_level_filler,overwrite=False)
            
            wind_direction_filler =  pd.DataFrame(X.groupby(['site_id','day','month'])['wind_direction'].mean(),columns=['wind_direction'])
            X.update(wind_direction_filler,overwrite=False)
            
            wind_speed_filler =  pd.DataFrame(X.groupby(['site_id','day','month'])['wind_speed'].mean(),columns=['wind_speed'])
            X.update(wind_speed_filler,overwrite=False)
            
            # Step 1
            precip_depth_filler = X.groupby(['site_id','day','month'])['precip_depth_1_hr'].mean()
            # Step 2
            precip_depth_filler = pd.DataFrame(precip_depth_filler.fillna(method='ffill'),columns=['precip_depth_1_hr'])
            
            X.update(precip_depth_filler,overwrite=False)
            
            X = X.reset_index()
            X = X.drop(['datetime','day','week','month'],axis=1)
    
        return X