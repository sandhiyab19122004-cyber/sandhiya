import pandas as pd
import numpy as np

class DataAcquisition:
    def __init__(self):
        self.data_sources = {
            'epa': None,
            'oxford': None,
            'telematics': None
        }
        
    def load_epa_data(self, filepath):
        """Load EPA fuel economy data"""
        self.data_sources['epa'] = pd.read_csv(filepath)
        return self.data_sources['epa']
    
    def load_oxford_data(self, filepath):
        """Load Oxford vehicle database"""
        self.data_sources['oxford'] = pd.read_excel(filepath)
        return self.data_sources['oxford']
    
    def merge_datasets(self):
        """Merge all data sources on common identifiers"""
        merged_df = pd.merge(
            self.data_sources['epa'],
            self.data_sources['oxford'],
            on=['make', 'model', 'year'],
            how='inner'
        )
        return merged_df
    
    def add_external_factors(self, weather_data=None, traffic_data=None):
        """Incorporate external environmental factors"""
        if weather_data:
            merged_df = pd.merge(merged_df, weather_data, on=['region', 'date'])
        if traffic_data:
            merged_df = pd.merge(merged_df, traffic_data, on=['region', 'time_of_day'])
        return merged_df
