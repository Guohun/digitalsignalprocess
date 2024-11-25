# Use the sounddevice module
# http://python-sounddevice.readthedocs.io/en/0.3.10/


import time

import numpy as np
import sounddevice as sd
import soundfile as sf
try:
    #data, SAMPLE_RATE = sf.read('/Users/zhuguohun/Music/Liu2007/1 (43).wav', dtype='float32')
    #read the wav file
    sound_data, SAMPLE_RATE = sf.read('/Users/zhuguohun/Music/Liu2007/1 (110).wav', dtype='float32')
    duration_s=len(sound_data)/SAMPLE_RATE      #get the sound duration
    atten=max(sound_data)                       #get the maximum amplitutde
    N = np.ceil(SAMPLE_RATE * duration_s)       #四舍五入取整
    #play the sound
    sd.play(sound_data, SAMPLE_RATE)
    status = sd.wait()

    each_sample_number = np.arange(N)           #产生 0,1,2..N-1

    # 产生440 Hz的Sine  这个应用作为噪音
    freq_hz = 440.0
    waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / SAMPLE_RATE)
    waveform_nosie = waveform * atten + sound_data

    import matplotlib.pyplot as plt
    plt.subplot(211)
    plt.plot(sound_data[:10000])
    plt.xlabel("Cough time / samples")
    plt.ylim(-atten, atten);
    plt.subplot(212)
    plt.plot(waveform_nosie[:10000])
    plt.xlabel("Cough + Noise time / samples")
    plt.ylim(-atten, atten);
    plt.show()

    #play the noise sound
    sd.play(waveform_nosie[:10000], SAMPLE_RATE)
    status = sd.wait()
    sd.stop()

    from scipy.fft import fft, fftfreq, ifft
    yf = fft(waveform_nosie)
    xf = fftfreq(int(N), 1 / SAMPLE_RATE)
    list_s=np.abs(yf)
    plt.plot(xf, list_s)
    plt.show()

    max_val = max(list_s)
    idx_max = np.where(list_s==max_val)
    yf[idx_max]=0
    plt.plot(xf, np.abs(yf))
    plt.show()

    new_sig = np.real(ifft(yf))
    plt.plot(new_sig[:10000])
    plt.show()

    sd.play(new_sig[:10000], SAMPLE_RATE)
    status = sd.wait()
    sd.stop()

except KeyboardInterrupt:
    print('\nInterrupted by user')
    sd.stop()
except Exception as e:
    print(type(e).__name__ + ': ' + str(e))
if status:
    print('Error during playback: ' + str(status))



