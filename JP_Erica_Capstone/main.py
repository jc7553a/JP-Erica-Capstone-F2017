import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
import HPCP as HPCP
import MLP as net
import random as ra
import math
import sys
import os
import matplotlib.pylab as plt
from random import randint


def getData():
    path = 'C:\JP_Erica_Capstone\JP_Erica_Capstone\Data\AChord'
    path2 = 'C:\JP_Erica_Capstone\JP_Erica_Capstone\Data\DChord'
    path3 = 'C:\JP_Erica_Capstone\JP_Erica_Capstone\Data\GChord'

    AMajor = []
    for filename in os.listdir(path):
        holder = []
        holder.append(filename)
        holder.append([1])
        AMajor.append(holder)

    DMajor = []
    for filename in os.listdir(path2):
        holder = []
        holder.append(filename)
        holder.append([2])
        DMajor.append(holder)

    GMajor = []
    for filename in os.listdir(path3):
        holder = []
        holder.append(filename)
        holder.append([3])
        GMajor.append(holder)
        
    return AMajor, DMajor, GMajor


'''Running Harmonic Pitch Class Profile on Training Data'''
def getChroma(files, val):
    totalChroma = []
    for i in range(len(files)):
        totalChroma.append(HPCP.hpcp(files[0][0], val))
    
    return totalChroma
                           
'''Gets rid of Rows of 0's'''
def cleanUpChroma(chromaGiven):
    for i in range(len(chromaGiven)):
        j = 0
        while j < (len(chromaGiven[i])):
            if np.sum(chromaGiven[i][j]) == 0:
                np.delete(chromaGiven[i][j], j, axis = 0)
                j -= 1
            j+=1
    return chromaGiven

'''This is Wicked Dumb need to find a new way to append vals to end of
    Numpy Array'''
def addClassification(chromaGiven, val):
    chromaBack = []
    shape = np.shape(chromaGiven)
    for i in range(shape[0]):
        for j in range(shape[1]):
            holder = []
            for t in range(shape[2]):
                holder.append(chromaGiven[i][j][t]*100)
            holder.append(val)
            chromaBack.append(holder)
    return chromaBack

'''Train Neural Network'''
def trainNetwork(data):
    print("Training Network....")
    network = net.MLP(12, 15)
    np.random.shuffle(data)
    for i in range(5):
        for j in range(len(data)):
            rand = randint(0, len(data)-1)
            if np.sum(data[rand][0:12]) !=0:
                network.train([data[rand][0:12]], [[data[rand][12]]])
    return network


'''Testing Network'''        
def testNetwork(network, testingDataGiven):
    values = []
    for i in range(len(testingDataGiven)):
        values.append(network.calc_total_cost([testingDataGiven[i][0:12]], [[0]]))
    threshedValues = []
    for i in range(len(values)):
        if values[i] < 1.65:
            threshedValues.append(1)
        elif values[i] > 1.35 and values[i] < 2.7:
            threshedValues.append(2)
        elif values[i] > 2.5:
            threshedValues.append(3)
    
    return threshedValues
                    
                      
    
    

if __name__ == '__main__':
    AMajor, DMajor, GMajor = getData()
    AChroma = addClassification(getChroma(AMajor, 1),1)
    DChroma = addClassification(getChroma(DMajor, 2),2)
    GChroma = addClassification(getChroma(GMajor, 3),3)
    testingData = []
    testingData.append(AChroma[len(AChroma)-1])
    testingData.append(DChroma[len(DChroma)-1])
    testingData.append(GChroma[len(GChroma)-1])
    
    del AChroma[len(AChroma)-1]
    del DChroma[len(DChroma)-1]
    del GChroma[len(GChroma)-1]
    
    totalData = np.concatenate((np.array(AChroma), np.array(DChroma)))
    totalData = np.concatenate((totalData, np.array(GChroma)))
    
    neuralNetwork = trainNetwork(totalData)
    testingValues = testNetwork(neuralNetwork, cleanUpChroma(testingData))
    falseAChord = 0
    AChordCorrect = 0
    falseDChord = 0
    
    DChordCorrect = 0
    falseGChord = 0
    GChordCorrect = 0
    actual = []

    for i in range(len(testingValues)):
        if testingValues[i] == 1 and testingData[i][12] == 1:
            AChordCorrect += 1
        if testingValues[i] != 1 and testingData[i][12] == 1:
            falseAChord += 1
        if testingValues[i] == 2 and testingData[i][12] == 2:
            DChordCorrect += 1
        if testingValues[i] != 2 and testingData[i][12] == 2:
            falseDChord +=1
        if testingValues[i] == 3 and testingData[i][12] == 3:
            GChordCorrect += 1
        if testingValues[i] != 3 and testingData[i][12] == 3:
            falseGChord +=1


    print(falseAChord)
    print(AChordCorrect)
    print(falseDChord)
    print(DChordCorrect)
    print(falseGChord)
    print(GChordCorrect)
    
