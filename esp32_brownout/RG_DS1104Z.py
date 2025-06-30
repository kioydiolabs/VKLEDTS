#  Copyright (C) 2025 Stratos Thivaios
#
#  This file is part of "VKLEDTS", a repository of instrument test scripts.
#
#  VKLEDTS is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
from io import BytesIO

from fontTools.ttLib.woff2 import bboxFormat
from matplotlib.pyplot import margins

import visares
import psytestbench
import time
import numpy as np
import os
import datetime

# user input
title = str(input("Title for the figures/graphs > "))
copyrightNotice = str(input("If you want a copyright notice on the graph enter it now > "))
try:
    triggerLevInput = input("What level should the oscilloscope trigger (CH2/3V3) [DEFAULT IS 2.75v] > ")
    if triggerLevInput == "":
        print("Defaulting to 2.75v")
        triggerLev = 2.75
    else:
        triggerLev = float(triggerLevInput)
    intervalBetweenTests = float(input("How long should the interval between tests be > "))
    numberOfTests = int(input("How many tests should be carried out > "))
except ValueError:
    print("Whatever you entered is not a number.")
    exit()

bwFilterInput = input("Should the BW filter be enabled on both channels [Y/n] > ")
if triggerLevInput.lower() == "y":
    print("BW filter will be enabled")
    bwFilter = True
else:
    bwFilter = False

dirname = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs(dirname)
i = 1

# instantiate
dso = psytestbench.ds1000z.instrument.Instrument(visares.lab_scope)
try:
    dso.connect()
except Exception as e:
    print("Fatal error while attempting to connect to the instrument. More details below:")
    raise e

while i >= 10:
    # clear, set trigger to auto, and run the scope
    dso.clear()
    dso.trigger.auto()
    dso.run()

    # timebase and scale and offset
    dso.timebase.scale(0.01)
    dso.channel1.scale(0.5)
    dso.channel2.scale(0.5)
    dso.channel1.offset(-3.4)
    dso.channel2.offset(-3.9)
    dso.timebase.offset(0.25)

    # configure channels and trigger
    dso.channel1.couplingDC()
    dso.channel1.on()
    dso.channel2.couplingDC()
    dso.channel2.on()
    if bwFilter:
        dso.channel1.bandwidthLimit20MHz()
        dso.channel2.bandwidthLimit20MHz()
    else:
        dso.channel1.bandwidthLimitOff()
        dso.channel2.bandwidthLimitOff()
    dso.trigger.modeEdge()
    dso.trigger.edge.source(dso.channel2)
    dso.trigger.edge.slope('FALL')
    dso.trigger.edge.level(triggerLev)

    # enable vmin measurements on both channels
    dso.measure.vMin(dso.channel1)
    dso.measure.vMin(dso.channel2)

    # set trigger to auto mode
    dso.trigger.single()

    print(f"\n({i}/10) Waiting to trigger", end="")
    timeout = time.time() + 25
    while time.time() < timeout:
        if dso.trigger.statusIsStop():
            triggerTimeString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
        print(".", end="")
        time.sleep(0.1)
    else:
        dso.disconnect()
        raise RuntimeError("\n\nTimeout waiting for brownout trigger")

    # pull the measurement values
    vMinC1 = dso.measurement.vMin(dso.channel1)
    vMinC2 = dso.measurement.vMin(dso.channel2)

    dso.write(":WAVeform:FORMat ASCii")
    time.sleep(1)
    dso.write(":WAVeform:SOURce CHANnel1")
    rawC1 = dso.query(":WAVeform:DATA?")
    dso.write(":WAVeform:SOURce CHANnel2")
    rawC2 = dso.query(":WAVeform:DATA?")
    preamble = dso.query(":WAVeform:PREamble?")

    fmt, typ, pts, xinc, xorig, xref, yinc, yorig, yref, _ = preamble.split(',')

    pts = int(pts)
    xinc = float(xinc)  # seconds per point
    xorig = float(xorig)  # time offset
    yinc = float(yinc)  # volts per ADC count
    yorig = float(yorig)  # voltage offset

    # 3) Chop off any SCPI block header (#<d><len>)
    if rawC1.startswith('#'):
        n_digits = int(rawC1[1])
        rawC1 = rawC1[2 + n_digits:]

    # 4) Convert to Python floats
    ch1voltages = [float(val) for val in rawC1.split(',')]

    # 3) Chop off any SCPI block header (#<d><len>)
    if rawC2.startswith('#'):
        n_digits = int(rawC2[1])
        rawC2 = rawC2[2 + n_digits:]

    # 4) Convert to Python floats
    ch2voltages = [float(val) for val in rawC2.split(',')]

    # 5) Build a time axis from the preamble
    times = [i * xinc + xorig for i in range(pts)]

    # 6) Plot
    import matplotlib.pyplot as plt

    plt.figure(figsize=(18, 9))
    plt.gcf().patch.set_facecolor('#151515')
    plt.gca().set_facecolor("#151515")
    plt.plot(times, ch1voltages, color='yellow', label='CH1 (5V)')  # lime green for CH1
    plt.plot(times, ch2voltages, color='cyan', label='CH2 (3V3)')  # cyan for CH2
    plt.axhline(triggerLev, color='orange', linestyle='--', linewidth=1.0, label='Trigger Level (CH2)')
    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (V)")

    min_val1 = np.min(ch1voltages)
    min_idx1 = np.argmin(ch1voltages)
    min_time1 = times[min_idx1]
    plt.plot(min_time1, min_val1, marker='x', color='red', markersize=12, label='CH1 Min')

    min_val2 = np.min(ch2voltages)
    min_idx2 = np.argmin(ch2voltages)
    min_time2 = times[min_idx2]
    plt.plot(min_time2, min_val2, marker='x', color='green', markersize=12, label='CH2 Min')

    plt.legend(loc='upper right', facecolor='#151515', edgecolor='white', labelcolor='white')

    # Display the value in the bottom left corner of the plot
    plt.text(0.015, 0.03,
             f"CH1 Min: {min_val1:.2f}V at {min_time1:.1f}ms\nCH2 Min: {min_val2:.2f}V at {min_time2:.1f}ms",
             transform=plt.gca().transAxes,
             color='white', fontsize=12,  # bigger font & white for contrast on dark bg
             verticalalignment='bottom', horizontalalignment='left',
             bbox=dict(facecolor='gray', edgecolor='none', boxstyle='square,pad=0.3', alpha=0.9))

    plt.text(0.985, 0.03,
             f"Copyright © KioydioLabs 2025",
             transform=plt.gca().transAxes,
             color='white', fontsize=12,  # bigger font & white for contrast on dark bg
             verticalalignment='bottom', horizontalalignment='right',
             bbox=dict(facecolor='gray', edgecolor='none', boxstyle='square,pad=0.3', alpha=0.9))

    plt.gca().xaxis.label.set_color('white')
    plt.gca().yaxis.label.set_color('white')
    plt.gca().tick_params(colors='white')  # ticks and tick labels white

    if not title == "":
        finalTitle = f"{title} | Test #{i}"
    else:
        finalTitle = f"Test #{i}"
    plt.suptitle(finalTitle, fontsize=28, fontweight='bold', color='white')
    plt.title(f"Triggered at {triggerTimeString}", fontsize=14, color='gray')
    plt.grid(True, color="white", linewidth=1, linestyle="--")

    plt.show()
    exit()
    # plt.savefig(f"{dirname}/TEST_{i}.png")

    i+=1

# disconnect from scope so that it doesn't explode
dso.disconnect()
print("Disconnected from oscilloscope")