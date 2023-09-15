from sim900Lib import SIM900

sim = SIM900("/dev/ttyUSB0",19200,1)
sim.connect()

while True:
    try:
        sim.parseResponse()
    except:
        print("Lost track. Retrying...")
        continue
    
sim.flush()
sim.disconnect()