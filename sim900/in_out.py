import threading
from sim900Lib import SIM900

sim = SIM900("/dev/ttyUSB0", 19200, 1)
sim.connect()

def receive_sms():
    while True:
        sim.receiveSMS()

def download_and_send_messages():
    while True:
        sim.parseResponse()

# Create and start the threads
receive_thread = threading.Thread(target=receive_sms)
receive_thread.start()

download_thread = threading.Thread(target=download_and_send_messages)
download_thread.start()

# Wait for the threads to complete (if needed)
receive_thread.join()
download_thread.join()

sim.flush()
sim.disconnect()

