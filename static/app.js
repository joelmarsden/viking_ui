class SensorMonitor {
    constructor() {
        this.updateInterval = 1000;
        this.isRunning = false;
        this.init();
        this.initSettings();
    }

    init() {
        this.startMonitoring();
        this.updateStatus('connected');
    }

    initSettings() {
        const settingsBtn = document.getElementById('settings-btn');
        const modal = document.getElementById('settings-modal');
        const closeBtn = document.getElementById('close-settings');
        const cancelBtn = document.getElementById('cancel-settings');
        const saveBtn = document.getElementById('save-settings');

        settingsBtn.addEventListener('click', () => this.openSettings());
        closeBtn.addEventListener('click', () => this.closeSettings());
        cancelBtn.addEventListener('click', () => this.closeSettings());
        saveBtn.addEventListener('click', () => this.saveSettings());

        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.closeSettings();
        });
    }

    async openSettings() {
        try {
            const response = await fetch('/api/settings');
            const settings = await response.json();
            
            document.getElementById('temp-threshold-input').value = settings.TEMPERATURE_THRESHOLD;
            document.getElementById('hr-threshold-input').value = settings.HEART_RATE_THRESHOLD;
            document.getElementById('gforce-threshold-input').value = settings.GFORCE_THRESHOLD;
            
            document.getElementById('settings-modal').style.display = 'block';
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }

    closeSettings() {
        document.getElementById('settings-modal').style.display = 'none';
    }

    async saveSettings() {
        const tempThreshold = parseFloat(document.getElementById('temp-threshold-input').value);
        const hrThreshold = parseInt(document.getElementById('hr-threshold-input').value);
        const gforceThreshold = parseFloat(document.getElementById('gforce-threshold-input').value);

        try {
            const response = await fetch('/api/settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    TEMPERATURE_THRESHOLD: tempThreshold,
                    HEART_RATE_THRESHOLD: hrThreshold,
                    GFORCE_THRESHOLD: gforceThreshold
                })
            });

            const result = await response.json();
            
            if (response.ok) {
                // Update displayed thresholds
                document.getElementById('temp-threshold').textContent = tempThreshold;
                document.getElementById('hr-threshold').textContent = hrThreshold;
                document.getElementById('gforce-threshold').textContent = gforceThreshold;
                
                this.closeSettings();
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error saving settings:', error);
            alert('Error saving settings. Please try again.');
        }
    }

    async fetchSensorData() {
        try {
            const response = await fetch('/api/sensor-data');
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('Error fetching sensor data:', error);
            this.updateStatus('error');
            return null;
        }
    }

    updateDisplay(data) {
        if (!data) return;

        // Update temperature
        document.getElementById('temperature').textContent = data.temperature.toFixed(1);
        const tempCard = document.getElementById('temperature-card');
        this.toggleWarning(tempCard, data.warnings.temperature);

        // Update heart rate
        document.getElementById('heart-rate').textContent = data.heart_rate;
        const hrCard = document.getElementById('heart-rate-card');
        this.toggleWarning(hrCard, data.warnings.heart_rate);

        // Update G-Force
        document.getElementById('gforce').textContent = data.gforce.toFixed(1);
        const gforceCard = document.getElementById('gforce-card');
        this.toggleWarning(gforceCard, data.warnings.gforce);

        // Update gyroscope
        // document.getElementById('gyro-x').textContent = data.gyroscope.x.toFixed(2);
        // document.getElementById('gyro-y').textContent = data.gyroscope.y.toFixed(2);
        // document.getElementById('gyro-z').textContent = data.gyroscope.z.toFixed(2);
        //
        // // Update accelerometer
        // document.getElementById('accel-x').textContent = data.accelerometer.x.toFixed(2);
        // document.getElementById('accel-y').textContent = data.accelerometer.y.toFixed(2);
        // document.getElementById('accel-z').textContent = data.accelerometer.z.toFixed(2);

        // Update timestamp
        const now = new Date();
        document.getElementById('last-update').textContent = now.toLocaleTimeString();

        this.updateStatus('connected');
    }

    toggleWarning(element, isWarning) {
        if (isWarning) {
            element.classList.add('warning');
        } else {
            element.classList.remove('warning');
        }
    }

    updateStatus(status) {
        const statusElement = document.getElementById('status');
        switch(status) {
            case 'connected':
                statusElement.style.color = '#4CAF50';
                break;
            case 'error':
                statusElement.style.color = '#f44336';
                break;
            default:
                statusElement.style.color = '#ff9800';
        }
    }

    async updateSensorData() {
        const data = await this.fetchSensorData();
        this.updateDisplay(data);
    }

    startMonitoring() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.updateSensorData();
        
        this.intervalId = setInterval(() => {
            this.updateSensorData();
        }, this.updateInterval);
    }

    stopMonitoring() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        this.isRunning = false;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SensorMonitor();
});
