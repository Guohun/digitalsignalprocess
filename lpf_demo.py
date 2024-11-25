'''
A demo for RC low-pass  digital filter

'''

import time

import numpy as np
import sounddevice as sd
import soundfile as sf

def lpf(x, omega_c , R, C):
    """Implement a digital R C low-pass filter.
    x input signal
    omega_c    T* pi
    R, C  on the cirucit
    """
    y = x
    beta =1 - np.exp(- omega_c / (R*C))
    print("beta", beta)
    for k in range(1, len(x)):
        y[k] = (1-beta) * y[k - 1] + beta * x[k]        ##(1-b)y(n-1)+b x(n)
    return y

Duration = 5                                 #时长
T = 0.02                                     #采样周期   采样周期不同，滤波参数不同
t = np.arange(0.0, Duration, T)

f_1 = 0.5                                    #Hz
f_2 = 9                                      #noise Hz
x_1 = np.sin(2.0 * np.pi * f_1 * t)
x_2 = np.sin(2.0 * np.pi * f_2 * t)

import matplotlib.pyplot as plt

plt.subplot(311)
plt.plot(t, x_1)
plt.ylabel("$x_1(t)$")
plt.setp(plt.gca(), xticklabels=[])
plt.subplot(312)
plt.plot(t, x_2)
plt.ylabel("$x_2(t)$")
plt.setp(plt.gca(), xticklabels=[])
plt.subplot(313)
plt.plot(t, x_1 + x_2, alpha=0.5, label="$x_1+x_2$")
plt.plot(t, x_1, label="$x_1$ (low-frequency signal)")
plt.xlabel("$t$ [s]")
plt.ylabel("$x(t)$")
plt.legend()
plt.show()


#play the noise sound
#    sd.play(waveform_nosie[:10000], SAMPLE_RATE)
#    status = sd.wait()
#    sd.stop()

R=10* pow(10,3)
C1=10* pow(10,-6)                   #   10u
C2=100* pow(10,-6)                  #   100u
omega_c = T* np.pi
y1 = lpf(x_1 + x_2, omega_c,R,C1)
y2 = lpf(x_1 + x_2, omega_c,R,C2)

plt.subplot(311)
plt.plot(t, x_1 + x_2, alpha=0.5, label="$x_1+x_2$ (input)")
plt.plot(t, x_1, label="$x_1$ (low-frequency signal)")
plt.ylabel("$x(t)$")
plt.setp(plt.gca(), xticklabels=[])
plt.legend()
plt.subplot(312)
plt.plot(t, y1, alpha=0.5, label="$C_1=10u$ (filtered output)")
plt.plot(t, x_1, label="$x_1$ (low-frequency signal)")
plt.xlabel("$t$ [rad/s]")
plt.ylabel("$y(t)$")
plt.legend()
plt.subplot(313)
plt.plot(t, y2, alpha=0.5, label="$C_2=100u$ (filtered output)")
plt.plot(t, x_1, label="$x_1$ (low-frequency signal)")
plt.xlabel("$t$ [rad/s]")
plt.ylabel("$y(t)$")
plt.legend()
plt.show()


#sd.play(new_sig[:10000], SAMPLE_RATE)
#status = sd.wait()
#sd.stop()
