from sim900Lib import SIM900

sim = SIM900("/dev/ttyUSB0",19200,1.0)
sim.connect()
sim.call("+250788862399")
sim.flush()
sim.disconnect()
