from flask import Flask, request, jsonify
import joblib

class EmissionsAPI:
    def __init__(self, model_path='trained_emissions_model.pkl'):
        self.app = Flask(__name__)
        self.model = joblib.load(model_path)
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/predict', methods=['POST'])
        def predict():
            try:
                vehicle_data = request.json
                predictor = EmissionsPredictor(self.model)
                result = predictor.generate_report(pd.DataFrame([vehicle_data]))
                return jsonify(result), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 400
                
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'healthy'}), 200
            
    def run(self, debug=True, port=5000):
        self.app.run(debug=debug, port=port)
