from sim900Lib import SIM900

sim = SIM900("/dev/ttyUSB0",19200,1)
sim.connect()
sim.receiveSMS()
sim.flush()
sim.disconnect()