import psytestbench
import time

# instantiate
dso =  psytestbench.ds1000z.instrument.Instrument('USB0::0x1AB1::0x04CE::DS1ZC264102595::INSTR')
dso.connect()

# timebase and scale and offset
dso.timebase.scale(0.01)
dso.channel1.scale(0.5)
dso.channel2.scale(0.5)
dso.channel1.offset(-3.4)
dso.channel2.offset(-3.9)

# configure channels and trigger
dso.channel1.couplingDC()
dso.channel1.on()
dso.channel2.couplingDC()
dso.channel2.on()
dso.trigger.modeEdge()
dso.trigger.edge.source(dso.channel2)
dso.trigger.edge.slope('FALL')
dso.trigger.edge.level(2.75)

# set trigger to auto mode
dso.trigger.single()

timeout = time.time() + 10
while time.time() < timeout:
    if dso.trigger.statusIsStop():
        break
    time.sleep(0.5)
else:
    dso.disconnect()
    raise RuntimeError("Timeout waiting for brownout trigger")

# enable vmin measurements on both channels
dso.measure.vMin(dso.channel1)
dso.measure.vMin(dso.channel2)

# pull the measurement values
vMinC1 = dso.measurement.vMin(dso.channel1)
vMinC2 = dso.measurement.vMin(dso.channel2)

# print em out
print(vMinC1, vMinC2)

# disconnect from scope so that it doesn't explode
dso.disconnect()