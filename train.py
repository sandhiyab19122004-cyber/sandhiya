from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score

class EmissionsModel:
    def __init__(self):
        self.model = None
        self.features = []
        self.target = 'co2_emissions'
        
    def prepare_data(self, dataframe, test_size=0.2):
        """Split data into training and testing sets"""
        X = dataframe[self.features]
        y = dataframe[self.target]
        return train_test_split(X, y, test_size=test_size, random_state=42)
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost regression model"""
        self.model = XGBRegressor(
            n_estimators=1000,
            learning_rate=0.01,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        self.model.fit(X_train, y_train)
        
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        predictions = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        cv_scores = cross_val_score(self.model, X_test, y_test, cv=5, scoring='neg_mean_absolute_error')
        
        print(f"MAE: {mae:.2f} g/km")
        print(f"R² Score: {r2:.4f}")
        print(f"Cross-Validation MAE: {-np.mean(cv_scores):.2f} ± {np.std(cv_scores):.2f} g/km")
        
    def get_feature_importance(self):
        """Extract feature importance scores"""
        importance = pd.DataFrame({
            'feature': self.features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        return importance
