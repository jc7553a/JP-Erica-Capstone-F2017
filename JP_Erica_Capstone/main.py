import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
import HPCP as HPCP
import MLP as net
import random as ra



chroma = HPCP.hpcp('AMajor.wav')
print(np.shape(chroma))
chroma2 = HPCP.hpcp('DMajor7.wav')
chroma3 = HPCP.hpcp('AMajorTest.wav')

vals = []
for i in range(len(chroma)):
    holder = []
    for j in range(len(chroma[i])):
        holder.append(chroma[i][j])
    holder.append([1,1])
    vals.append(holder)
#print(vals[1][0:12])
for i in range(len(chroma2)):
    holder = []
    for j in range(len(chroma2[i])):
        holder.append(chroma2[i][j])
    holder.append([5,5])
    vals.append(holder)

network = net.MLP(12, 15)
np.random.shuffle(vals)

print(vals[0][0:12])

total = len(chroma2)+len(chroma)
for t in range(400):
    for i in range(total):
        rand = ra.randint(0, len(vals)-1)
        network.train([vals[rand][0:12]], [vals[rand][12]])


print(network.output([chroma[1]]))

print(network.output([chroma2[20]]))
print(network.output([chroma3[4]]))
