# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import pylab as plt
import h5py as hp


# Loading the profile
filename = r'./prof.h5'
h5file = hp.File(filename, 'r') 
profile = np.array(h5file["/Profile/profile"], dtype = np.double)
samplerate = float(h5file["/Profile/samplerate"][0])
recordlength = int(h5file["/Profile/record_length"][0])
h5file.close()

time = np.arange(recordlength) / samplerate
profile = profile.mean(1)

dt = time[1]-time[0]
noints = time.shape[0]

# Extending the time array to improve the deconvolution
time = np.arange(time.min(),time.max()+100e-9,dt)
profile = np.concatenate((profile,np.zeros(time.shape[0]-noints)))

# Recalculate the number of points and the frequency array
noints = time.shape[0]
freq = np.fft.fftfreq(noints,d=dt)

# Load the transfer function and interpolate to the frequency array
beam = 1
h5file = hp.File(r'tf.h5', 'r') 
freq_array = np.array(h5file["/TransferFunction/freq"])
TF_array = np.array(h5file["/TransferFunction/TF"])
h5file.close()
TF = np.interp(freq, np.fft.fftshift(freq_array), np.fft.fftshift(TF_array.real)) + \
     1j * np.interp(freq, np.fft.fftshift(freq_array), np.fft.fftshift(TF_array.imag))
     
# Remove zeros in high-frequencies
TF[TF==0] = 1.0+0j

# Deconvolution
filtered_f = np.fft.fft(profile)/TF
filtered = np.fft.ifft(filtered_f).real
filtered -= filtered[:10].mean()

## Plots
plt.figure()
plt.plot(time*1e9,profile/profile.max(0),lw=2,label='Measured')
plt.plot(time*1e9,filtered/max(filtered),lw=2,label='Deconvolved')
plt.xlabel('Time [ns]')
plt.legend(loc=0)
plt.show()
input()
