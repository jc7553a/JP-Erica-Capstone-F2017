import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
import HPCP as HPCP
import MLP as net
import random as ra
import math


'''Computing Harmonic Pitch Class Profile for Each Wav File'''
chroma = HPCP.hpcp('AMajor.wav')
print(np.shape(chroma))
chroma2 = HPCP.hpcp('DMajor7.wav')
chroma3 = HPCP.hpcp('AMajorTest.wav')

'''These Two Loops just attach a Class Value to the end of Array'''
'''[1,1] Corresponds to AMajor Chord'''
'''[2,2] Corresponds to DMajor7 Chord'''
'''I shouldn't be using Major 7ths but I like them theyre cool'''


vals = []
for i in range(len(chroma)):
    holder = []
    for j in range(len(chroma[i])):
        holder.append(math.ceil(chroma[i][j]))
    holder.append([1,1])
    vals.append(holder)

for i in range(len(chroma2)):
    holder = []
    for j in range(len(chroma2[i])):
        holder.append(math.ceil(chroma2[i][j]))
    holder.append([2,2])
    vals.append(holder)


'''Building Neural Network'''
network = net.MLP(12, 15)

'''Shuffling up the Data'''
np.random.shuffle(vals)

'''Training the Network with 400 Epochs'''
total = len(chroma2)+len(chroma)
for t in range(400):
    for i in range(total):
        rand = ra.randint(0, len(vals)-1)
        network.train([vals[rand][0:12]], [vals[rand][12]])


'''Testing the network With AMajorTest.wav'''
'''This isn't a great way to test but just getting a feel'''
'''We will soon need to make threshold determinations for each chord'''
print("Length ", len(chroma3))
numnum = 0
for i in range(len(chroma3)):
    jp = network.output([chroma3[i]])
    avg = np.average(jp)
    if avg < 2:
        numnum +=1

'''The amount Classified Correctly then Accuracy'''
print("Correct ", numnum)
print("ACC ", numnum/len(chroma3))


