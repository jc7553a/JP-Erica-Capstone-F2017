import numpy as np
from scipy.io import wavfile
from scipy.sparse import coo_matrix
from scipy.signal import spectrogram, convolve2d
from scipy.fftpack import fft
import json
import sys
import os
import matplotlib.pyplot as plt



os.chdir('C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/TestSong')

win_size = 4096
window = 'hamming'
hop_size = 1024
print(win_size - hop_size)
sr, y = wavfile.read('SR001XY.wav')
x = fft(y)


print(sr)
print(len(y))

print( win_size > (win_size)/4)
if len(y.shape) > 1:
    y = np.mean(y, axis=1)

    # normalize
y = y/np.max(y)

X = fft(y)
plt.plot(X)
plt.show()

f, t, X = spectrogram(y, sr,nperseg = win_size, noverlap = win_size-hop_size ,  window=window)

X = X.astype('float32').T
shape = np.shape(X)
averageX = []
for i in range(shape[0]):
    averageX.append(np.average(X[i]))
newX = []
for j in range(len(averageX)):
    if averageX[j] > .0000015:
        newX.append(X[j][:])
print(np.shape(X))
plt.plot(X[0][0:100])
plt.show()
plt.plot(averageX)
plt.show()
plt.plot(newX)
plt.show()

k = np.arange(len(f))

f_min = 100
f_max = 5000
f_band = np.all([f >f_min, f < f_max], axis= 0)
Y_lim = (X[:, f_band])
k = k[f_band]
f = f[f_band]


