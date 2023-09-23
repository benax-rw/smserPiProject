from sim900Lib import SIM900

sim = SIM900("/dev/ttyUSB0",19200,1)
sim.connect()
sim.sendSMS("+250788862399", "Hello. It's me!")
sim.flush()
sim.disconnect()