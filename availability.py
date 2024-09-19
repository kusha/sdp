import time
import threading

from sdp import rings, probe_port

# run availability check in background
def track_availability():
    succ = 0
    fail = 0
    iterations = 0
    while True:
        for ring in rings:
            ring_idx = rings.index(ring) + 1
            failover_port = f"79{ring_idx}0"
            if probe_port(failover_port):
                succ += 1
            else:
                fail += 1
        time.sleep(1)
        iterations += 1
        if iterations % 5 == 0: # every 15 seconds
            print(f"Availability: {succ / (succ + fail) * 100:.2f}%")

track_availability_thread = threading.Thread(target=track_availability)
track_availability_thread.daemon = True
track_availability_thread.start()

while True:
    time.sleep(1)
