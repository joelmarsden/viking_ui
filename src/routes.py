from flask import Blueprint, render_template, jsonify, request
from src.sensor_data import SensorService
from src.settings import app_settings

main_bp = Blueprint('main', __name__)
sensor_service = SensorService()

@main_bp.route('/')
def index():
    return render_template('index.html', settings=app_settings)

@main_bp.route('/api/sensor-data')
def get_sensor_data():
    reading = sensor_service.get_current_reading()
    
    return jsonify({
        'temperature': reading.temperature,
        'heart_rate': reading.heart_rate,
        'gyroscope': reading.gyroscope,
        'accelerometer': reading.accelerometer,
        'gforce': reading.gforce,
        'warnings': {
            'temperature': app_settings.is_temperature_warning(reading.temperature),
            'heart_rate': app_settings.is_heart_rate_warning(reading.heart_rate),
            'gforce': app_settings.is_gforce_warning(reading.gforce)
        },
        'timestamp': reading.timestamp
    })

@main_bp.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(app_settings.to_dict())

@main_bp.route('/api/settings', methods=['POST'])
def update_settings():
    try:
        data = request.get_json()
        
        # Validate input
        if 'TEMPERATURE_THRESHOLD' in data:
            temp = float(data['TEMPERATURE_THRESHOLD'])
            if not (0.0 <= temp <= 100.0):
                return jsonify({'error': 'Temperature threshold must be between 0-100°C'}), 400
        
        if 'HEART_RATE_THRESHOLD' in data:
            hr = int(data['HEART_RATE_THRESHOLD'])
            if not (0 <= hr <= 220):
                return jsonify({'error': 'Heart rate threshold must be between 0-220 BPM'}), 400
        
        if 'GFORCE_THRESHOLD' in data:
            gf = float(data['GFORCE_THRESHOLD'])
            if not (0.0 <= gf <= 10.0):
                return jsonify({'error': 'G-Force threshold must be between 0.0-10.0g'}), 400
        
        app_settings.update_settings(**data)
        return jsonify({'success': True, 'settings': app_settings.to_dict()})
        
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input values'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
