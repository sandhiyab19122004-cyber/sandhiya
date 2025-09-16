class FeatureEngineering:
    def __init__(self, dataframe):
        self.df = dataframe
        
    def create_power_to_weight_ratio(self):
        """Calculate power-to-weight ratio"""
        self.df['power_to_weight'] = self.df['horsepower'] / self.df['weight']
        
    def encode_fuel_types(self):
        """One-hot encode fuel types"""
        fuel_dummies = pd.get_dummies(self.df['fuel_type'], prefix='fuel')
        self.df = pd.concat([self.df, fuel_dummies], axis=1)
        
    def calculate_age_factor(self):
        """Adjust for vehicle age efficiency degradation"""
        current_year = pd.Timestamp.now().year
        self.df['age_factor'] = 1 - ((current_year - self.df['year']) * 0.02)
        self.df['adjusted_emission_factor'] = self.df['emission_factor'] * self.df['age_factor'].clip(lower=0.7)
        
    def create_driving_condition_features(self, avg_speed, idle_time_pct):
        """Add driving condition parameters"""
        self.df['avg_speed'] = avg_speed
        self.df['idle_time_pct'] = idle_time_pct
        self.df['city-driving_factor'] = self.df['idle_time_pct'] * 1.2 + (100 - self.df['avg_speed']) * 0.001
