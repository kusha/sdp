import time
import threading
from collections import defaultdict

from sdp import rings, probe_port

# run availability check in background
def track_availability():
    succ = defaultdict(list)
    fail = defaultdict(list)
    iterations = 0
    while True:
        for ring in rings:
            ring_idx = rings.index(ring) + 1
            failover_port = f"79{ring_idx}0"
            if probe_port(failover_port):
                succ[ring].append(time.time())
            else:
                fail[ring].append(time.time())
        time.sleep(1)
        iterations += 1
        if iterations % 5 == 0: # every 15 seconds
            log = ""
            for ring in rings:
                ring_succ = succ[ring]
                ring_fail = fail[ring]
                recent_succ = len([t for t in ring_succ if t > time.time() - 60])
                recent_fail = len([t for t in ring_fail if t > time.time() - 60])
                rate = recent_succ / (recent_succ + recent_fail) * 100
                log += f"[{ring}: {rate:.2f}% a({len(ring_succ)}:{len(ring_fail)}) r({recent_succ}:{recent_fail})] "
            print(log)

track_availability_thread = threading.Thread(target=track_availability)
track_availability_thread.daemon = True
track_availability_thread.start()

print("Rings: a,b,c. Report: availability (1min), all queries, recent queries (1min).")
while True:
    time.sleep(1)
