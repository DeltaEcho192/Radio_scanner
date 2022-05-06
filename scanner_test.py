import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers

#enumerate devices
results = SoapySDR.Device.enumerate()
for result in results: print(result)
timeout_us = int(5e6)
print("test")
#create device instance
#args can be user defined or from the enumeration result
args = dict(driver="rtlsdr")
sdr = SoapySDR.Device(args)

#query device info
print(sdr.listAntennas(SOAPY_SDR_RX, 0))
print(sdr.listGains(SOAPY_SDR_RX, 0))
freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
for freqRange in freqs: print(freqRange)

#apply settings
sdr.setSampleRate(SOAPY_SDR_RX, 0, 1e6)
sdr.setFrequency(SOAPY_SDR_RX, 0, 94.5e5)

#setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
sdr.activateStream(rxStream) #start streaming

#create a re-usable buffer for rx samples
buff = numpy.array([0]*16384, numpy.complex64)

#receive some samples
sr = sdr.readStream(rxStream, [buff], len(buff),timeoutUs=timeout_us)


#shutdown the stream
sdr.deactivateStream(rxStream) #stop streaming
sdr.closeStream(rxStream)

S = np.fft.fftshift(np.fft.fft(s, N) / N)

# Time Domain Plot
plt.figure(num=1, figsize=(12.95, 7.8), dpi=150)
plt.subplot(211)
t_us = np.arange(N) / fs / 1e-6
plt.plot(t_us, s.real, 'k', label='I')
plt.plot(t_us, s.imag, 'r', label='Q')
plt.xlim(t_us[0], t_us[-1])
plt.xlabel('Time (us)')
plt.ylabel('Normalized Amplitude')

# Frequency Domain Plot
plt.subplot(212)
f_ghz = (freq + (np.arange(0, fs, fs/N) - (fs/2) + (fs/N))) / 1e9
plt.plot(f_ghz, 20*np.log10(np.abs(S)))
plt.xlim(f_ghz[0], f_ghz[-1])
plt.ylim(-100, 0)
plt.xlabel('Frequency (GHz)')
plt.ylabel('Amplitude (dBFS)')
plt.show()