# -*- coding: utf-8 -*-
"""GravitationalWave.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/wj198414/ASTRON1221/blob/main/GravitationalWave/GravitationalWave.ipynb
"""

import gwpy
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from gwpy.signal import filter_design
from gwpy.plot import Plot

"""The following example is from: https://gwpy.github.io/docs/stable/examples/signal/gw150914/"""

# Set a GPS time:
t0 = 1126259462.4    # -- GW150914
window = 32
# t0 = 1187008882.4    # -- GW170817

#Fetch LIGO data for [window] days around [t0]
hdata = TimeSeries.fetch_open_data('H1', t0 - window, t0 + window)

# Plot ASD
# Fourier transform data and find strongest constituent frequencies 
fig2 = hdata.asd(fftlength=8).plot()
plt.xlim(10,2000)
ymin = 1e-24
ymax = 1e-19
plt.ylim(ymin, ymax)

# 60Hz is frequency of interference from North American electrical grid
# We need to filter out these frequencies
plt.vlines(60, ymin, ymax, linestyle="dashed", color="red")
plt.vlines(120, ymin, ymax, linestyle="dashed", color="red")
plt.vlines(180, ymin, ymax, linestyle="dashed", color="red")

# We want to focus on the frequencies from 50 to 150
# Create filter for area between these frequencies
bp = filter_design.bandpass(50, 250, hdata.sample_rate)

# Create filter with notches at 60, 120 and 180
notches = [filter_design.notch(line, hdata.sample_rate) for
           line in (60, 120, 180)]

# Merge filters
zpk = filter_design.concatenate_zpks(bp, *notches)

# Filter data
hfilt = hdata.filter(zpk, filtfilt=True)

hdata = hdata.crop(*hdata.span.contract(1))
hfilt = hfilt.crop(*hfilt.span.contract(1))

#Plot strain data from Hanford
plot = Plot(hdata, hfilt, figsize=[12, 6], separate=True, sharex=True,
            color='gwpy:ligo-hanford')
ax1, ax2 = plot.axes
ax1.set_title('LIGO-Hanford strain data around GW150914')
ax1.text(1.0, 1.01, 'Unfiltered data', transform=ax1.transAxes, ha='right')
ax1.set_ylabel('Amplitude [strain]', y=-0.2)
ax2.set_ylabel('')
ax2.text(1.0, 1.01, r'50-250\,Hz bandpass, notches at 60, 120, 180 Hz',
         transform=ax2.transAxes, ha='right')
plot.show()


#Plot zoomed in data
plot = hfilt.plot(color='gwpy:ligo-hanford')
ax = plot.gca()
ax.set_title('LIGO-Hanford strain data around GW150914')
ax.set_ylabel('Amplitude [strain]')
ax.set_xlim(t0 - .3, t0 +.3)
ax.set_xscale('seconds', epoch = t0)
plot.show()

x_val = plt.gca().lines[0].get_xdata()
y_val = plt.gca().lines[0].get_ydata()

ldata = TimeSeries.fetch_open_data('L1', 1126259446, 1126259478)
lfilt = ldata.filter(zpk, filtfilt=True)

# Adjust for time delay of gravitational wave travel between stations
lfilt.shift('6.9ms')
lfilt *= -1

plot = Plot(figsize=[12, 4])
ax = plot.gca()
ax.plot(hfilt, label='LIGO-Hanford', color='gwpy:ligo-hanford')
ax.plot(lfilt, label='LIGO-Livingston', color='gwpy:ligo-livingston')
ax.set_title('LIGO strain data around GW150914')
ax.set_xlim(t0 - .3, t0 +.3)
ax.set_xscale('seconds', epoch = t0)
ax.set_ylabel('Amplitude [strain]')
ax.set_ylim(-1e-21, 1e-21)
ax.legend()
plot.show()

"""
https://colab.research.google.com/github/losc-tutorial/quickview/blob/master/index.ipynb
Also from: https://gwpy.github.io/docs/stable/examples/signal/qscan/
"""

dt = 0.2  #-- Set width of q-transform plot, in seconds
hq = hfilt.q_transform(outseg=(t0-dt, t0+0.1))
fig4 = hq.plot()
ax = fig4.gca()
fig4.colorbar(label="Normalized energy")
ax.grid(False)
ax.set_yscale('log')

from scipy.io.wavfile import write
import numpy as np

amplitude = np.iinfo(np.int16).max

ind = np.where((x_val < (t0+1.5)) & (x_val > (t0-1.5)))
y = y_val[ind]
# y = y**3
y = y / np.max(y)
plt.plot(x_val[ind] - t0, (np.array(y) * amplitude).astype(np.int16))

fs = int(1 / np.median(np.diff(np.array(x_val[ind] - t0))))
print("fs = ", fs)
write("example.wav", fs, (np.array(y) * amplitude).astype(np.int16))


#files.download("example.wav")

"""Make C"""

samplerate = 44100; fs = 261.63 * 2.0
t = np.linspace(0., 1., samplerate)
amplitude = np.iinfo(np.int16).max
data = amplitude * np.sin(2. * np.pi * fs * t)
plt.plot(t, data)
plt.xlim(0, 0.1)

write("C.wav", samplerate, data.astype(np.int16))
#files.download("C.wav")

