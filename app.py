from flask import Flask
import random
import os
import time

# load features
FEATURES = []
for key, value in os.environ.items():
    if key.startswith('FEATURE_'):
        try:
            failure_rate = int(value)
            feature = {
                'name': key,
                'enabled': True,
                'failure_rate': failure_rate
            }
            FEATURES.append(feature)
        except ValueError:
            print(f"Warning: Invalid failure rate for {key}. Skipping this feature.")

print("Enabled features:")
for feature in FEATURES:
    if feature['enabled']:
        print(f"- {feature['name']}")
        
start_time = time.time()

app = Flask(__name__)

@app.route('/')
def feature_response():
    current_time = time.time()
    ticks = int(current_time - start_time)
    
    for feature in [f for f in FEATURES if f['enabled']]:
        for it in range(ticks):
            if random.random() < (ticks / feature['failure_rate'] ):
                return f"Internal Server Error: {feature['name']} failed at #{it} tick", 500
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7900, debug=True)
