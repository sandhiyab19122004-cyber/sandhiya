import shap

class EmissionsPredictor:
    def __init__(self, trained_model):
        self.model = trained_model
        
    def predict_single_vehicle(self, vehicle_data):
        """Make prediction for single vehicle instance"""
        return self.model.predict(vehicle_data)[0]
    
    def predict_batch(self, vehicle_dataframe):
        """Make predictions for batch of vehicles"""
        return self.model.predict(vehicle_dataframe)
    
    def explain_prediction(self, vehicle_data):
        """Generate SHAP explanation for single prediction"""
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(vehicle_data)
        return shap_values
    
    def generate_report(self, vehicle_data, actual_value=None):
        """Create detailed prediction report"""
        prediction = self.predict_single_vehicle(vehicle_data)
        shap_values = self.explain_prediction(vehicle_data)
        
        report = {
            'predicted_co2': prediction,
            'feature_contributions': dict(zip(vehicle_data.columns, shap_values[0])),
            'comparison_to_average': f"{prediction - 200:+.1f} g/km vs industry average"
        }
        
        if actual_value is not None:
            report['accuracy'] = f"{100 * (1 - abs(prediction - actual_value) / actual_value):.1f}%"
            
        return report
