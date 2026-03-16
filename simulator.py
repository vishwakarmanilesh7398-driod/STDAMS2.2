"""
simulator.py
Simulates real-time satellite telemetry data with random anomalies.
"""
import time
import random
import csv
from datetime import datetime

DATA_FILE = 'data/satellite.csv'

# Initial normal values
ALTITUDE = 400  # km
VELOCITY = 7.8  # km/s
SIGNAL = 90    # %


def generate_telemetry():
    """Generate normal telemetry with occasional anomalies."""
    global ALTITUDE, VELOCITY, SIGNAL
    # Normal drift
    ALTITUDE += random.uniform(-0.2, 0.2)
    VELOCITY += random.uniform(-0.01, 0.01)
    SIGNAL += random.uniform(-0.2, 0.2)

    # Inject anomaly randomly
    anomaly = random.random() < 0.20  # Chance thoda badha kar 20% kar di
    if anomaly:
        print("!!! ANOMALY DETECTED !!!") # Terminal mein check karne ke liye
        anomaly_type = random.choice(['altitude', 'velocity', 'signal'])
        if anomaly_type == 'altitude':
            # 5 ki jagah 15-20 ka jump dein taaki graph upar bhage
            ALTITUDE += random.choice([-20, 20]) 
        elif anomaly_type == 'velocity':
            VELOCITY += random.choice([-0.8, 0.8])
        elif anomaly_type == 'signal':
            # Signal ko ekdum gira dein (Critical warning ke liye)
            SIGNAL -= random.uniform(20, 30)

    # Clamp values
    ALTITUDE = max(350, min(ALTITUDE, 450))
    VELOCITY = max(7.0, min(VELOCITY, 8.5))
    SIGNAL = max(60, min(SIGNAL, 100))

    return {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'altitude': round(ALTITUDE, 2),
        'velocity': round(VELOCITY, 2),
        'signal_strength': round(SIGNAL, 2)
    }

def write_telemetry(row):
    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'altitude', 'velocity', 'signal_strength'])
        writer.writerow(row)

if __name__ == '__main__':
    print('Starting telemetry simulation...')
    while True:
        telemetry = generate_telemetry()
        write_telemetry(telemetry)
        print('Telemetry:', telemetry)
        time.sleep(5)
