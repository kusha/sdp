from flask import Flask
import random
import os
import time

def load_features():
    # load features
    features = []
    for key, value in os.environ.items():
        if key.startswith('FEATURE_'):
            try:
                failure_rate = int(value)
                feature = {
                    'name': key,
                    'enabled': True,
                    'failure_rate': failure_rate
                }
                features.append(feature)
            except ValueError:
                pass  # Ignore invalid values

    print("Enabled features:")
    for feature in features:
        if feature['enabled']:
            print(f"- {feature['name']}")
    return features

FEATURES = load_features()
            
start_time = time.time()

HOSTNAME = os.environ.get('HOSTNAME', 'unknown')
BROKEN_FEATURE = None
app = Flask(__name__)

@app.route('/')
@app.route('/health')
def health():
    global BROKEN_FEATURE
    current_time = time.time()
    ticks = int(current_time - start_time)
    
    for feature in [f for f in FEATURES if f['enabled']]:
        for it in range(ticks):
            if random.random() < (ticks / feature['failure_rate'] ):
                BROKEN_FEATURE = feature['name']
    
    if BROKEN_FEATURE:
        return f"FAIL {HOSTNAME}: {BROKEN_FEATURE} failed", 500
    return f"OK {HOSTNAME}", 200

@app.route('/break')
def broke():
    global BROKEN_FEATURE
    BROKEN_FEATURE = "BREAK_ENDPOINT"
    return "DONE", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7900, debug=True)
