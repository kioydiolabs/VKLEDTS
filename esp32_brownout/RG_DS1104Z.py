#  Copyright (C) 2025 Stratos Thivaios
#
#  This file is part of "VKLEDTS", a repository of instrument test scripts.
#
#  VKLEDTS is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

import visares
import psytestbench
import time

# instantiate
dso =  psytestbench.ds1000z.instrument.Instrument(visares.lab_scope)
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