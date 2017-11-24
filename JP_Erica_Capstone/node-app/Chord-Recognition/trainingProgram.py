import numpy as np
import HPCP as HPCP
import MLP as net
import random as ra
import math
import tensorflow as tf
import os
import matplotlib.pyplot as plt
from random import randint
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve


def getData():
    '''
    path = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/BChord'
    path2 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/BChord'
    path3 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/CChord'
    path4 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/DChord'
    path5 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/EChord'
    path6 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/FChord'
    path7 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/GChord'
    path8 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/TestSong'
    '''
    path = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/a'
    path2 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/am'
    path3 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/bm'
    path4 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/c'
    path5 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/d'
    path6 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/dm'
    path7 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/e'
    path8 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/em'
    path9 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/f'
    path10 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Guitar_Only/g'
    path11 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/TestSong'

    AMajor = []
    TestSong = []
    for filename in os.listdir(path):
        holder = []
        holder.append(filename)
        holder.append([1])
        AMajor.append(holder)
    AMinor = []
    TestSong = []
    for filename in os.listdir(path2):
        holder = []
        holder.append(filename)
        holder.append([2])
        AMinor.append(holder)
        
    BMinor = []
    for filename in os.listdir(path3):
        holder = []
        holder.append(filename)
        holder.append([3])
        BMinor.append(holder)

    CMajor = []
    for filename in os.listdir(path4):
        holder = []
        holder.append(filename)
        holder.append([1])
        CMajor.append(holder)

    DMajor = []
    for filename in os.listdir(path5):
        holder = []
        holder.append(filename)
        holder.append([2])
        DMajor.append(holder)

    DMinor = []
    for filename in os.listdir(path6):
        holder = []
        holder.append(filename)
        holder.append([2])
        DMinor.append(holder)

    EMajor = []
    for filename in os.listdir(path7):
        holder = []
        holder.append(filename)
        holder.append([1])
        EMajor.append(holder)

    EMinor = []
    for filename in os.listdir(path8):
        holder = []
        holder.append(filename)
        holder.append([1])
        EMinor.append(holder)
        
    FMajor = []
    for filename in os.listdir(path9):
        holder = []
        holder.append(filename)
        holder.append([1])
        FMajor.append(holder)

    GMajor = []
    for filename in os.listdir(path10):
        holder = []
        holder.append(filename)
        holder.append([3])
        GMajor.append(holder)
    
    TestSong = []
    for filename in os.listdir(path11):
        holder = []
        holder.append(filename)
        holder.append([1])
        TestSong.append(holder)
        
    return AMajor, AMinor, BMinor, CMajor, DMajor, DMinor, EMajor, EMinor, FMajor, GMajor, TestSong


'''Running Harmonic Pitch Class Profile on Training Data'''
def getChroma(files, val):
    totalChroma = []
    for i in range(len(files)):
        totalChroma.append(HPCP.hpcp(files[0][0], val))
    return totalChroma
                           
'''Gets rid of Rows of 0's'''
def cleanUpChroma(chromaGiven):
    chromaBack = np.array(chromaGiven)
    chromaBack2 = []
    for i in range(len(chromaBack)): 
        chromaBack2.append(chromaBack[i][~(chromaBack[i]==0).all(1)])
    return chromaBack2

'''This is Wicked Dumb need to find a new way to append vals to end of
    Numpy Array'''
def addClassification(chromaGiven, val):
    chromaBack = []
    shape = np.shape(chromaGiven)
    for i in range(shape[0]):
        for j in range(shape[1]):
            holder = []
            for t in range(shape[2]):
                holder.append(chromaGiven[i][j][t])
            holder.append(val)
            chromaBack.append(holder)
    return chromaBack

'''Train Neural Network'''
def trainNetwork(data, network):
    print("Training Network....")
    #np.random.shuffle(data)
    losses = []
    num = 0
    for i in range(5):
        midLosses = []
        for j in range(len(data)):
            rand = randint(0, len(data)-1)
            midLosses.append(network.train([data[rand][0:12]], [[data[rand][12]]]))
        losses.append(np.average(midLosses))
        print("Epoch " +str(i))
    plt.plot(losses)
    plt.show()
    print("Done Training")
    return network


'''Testing Network'''        
def testNetwork(network, testingDataGiven):
    values = []
    print("Testing Values...")
    for i in range(len(testingDataGiven)):
        values.append(network.calc_total_cost([testingDataGiven[i][0:12]], [[0]]))
    threshedValues = []
    for i in range(len(values)):
        if values[i] <= 1.5:
            threshedValues.append(1)
        elif values[i] > 1.5 and values[i] <= 2.5:
            threshedValues.append(2)
        elif values[i] > 2.5 and values[i]<= 3.5:
            threshedValues.append(3)
        elif values[i] > 3.5 and  values[i]<= 4.5:
            threshedValues.append(4)
        elif values[i] > 4.5 and values[i] <= 5.5 :
            threshedValues.append(5)
        elif values[i] > 5.5 and values[i] <= 6.5:
            threshedValues.append(6)
        elif values[i] > 6.5:
            threshedValues.append(7)
    print("Done Testing")
    return threshedValues


def testingResults(actual, predicted):
    y_pred = pd.Series(predicted, name = 'Predicted')
    y_act = pd.Series(actual, name = 'Actual')
    df_confusion = pd.crosstab(y_act, y_pred, rownames = ['Actual'], colnames = ['Predicted'], margins = True)
    return df_confusion

                      

def findMaxIndex(listGiven):
    maxNum = 0
    maxIndex = 0
    for j in range(len(listGiven)):
        if listGiven[j] > maxNum:
            maxNum = listGiven[j]
            maxIndex = j
    return maxIndex

def findMajority(listGiven):
    myArray = [0,0,0,0,0,0,0]
    for i in range(len(listGiven)):
        if listGiven[i] == 1:
            myArray[0] +=1
        elif listGiven[i] == 2:
            myArray[1] +=1
        elif listGiven[i] == 3:
            myArray[2] +=1
        elif listGiven[i] == 4:
            myArray[3] +=1
        elif listGiven[i] == 5:
            myArray[4] +=1
        elif listGiven[i] == 6:
            myArray[5] +=1
        elif listGiven[i] == 7:
            myArray[6] +=1
    print(myArray)
    majorityLeader = findMaxIndex(myArray)
    return majorityLeader+1
    
def batchTraining(A, Am, Bm, C, D, Dm, E, Em, F, G):
    network = net.MLP(12, 9, 7)
    losses = []
    batchSize = 5
    for j in range(800):
        midLosses = []
        for i in range(500):
            chord = randint(0,9)
            if chord == 0:
                val = randint(0, len(A)-batchSize)
                batch = np.array(A[val: val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
            elif chord == 1:
                val = randint(0, len(Am)-batchSize)
                batch = np.array(Am[val: val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
            elif chord == 2:
                val = randint(0, len(Bm)-batchSize)
                batch = np.array(Bm[val: val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
            elif chord == 3:
                val = randint(0, len(C)-batchSize)
                batch = np.array(C[val: val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
            elif chord == 4:
                val = randint(0, len(D)-batchSize)
                batch = np.array(D[val: val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
            elif chord == 5:
                val = randint(0, len(Dm)-batchSize)
                batch = np.array(Dm[val: val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
            elif chord == 6:
                val = randint(0, len(E)-batchSize)
                batch = np.array(E[val: val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
            elif chord == 7:
                val = randint(0, len(Em)-batchSize)
                batch = np.array(Em[val: val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
            elif chord == 8:
                val = randint(0, len(F)-batchSize)
                batch = np.array(F[val: val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
            elif chord == 9:
                val = randint(0, len(G)-batchSize)
                batch = np.array(G[val:val+batchSize])
                classification = batch[0][12]
                batch = batch[:, 0:12]
                
            midLosses.append(network.train(batch, [[classification]]))
        losses.append(np.average(midLosses))
    plt.plot(losses)
    plt.show()
    return network
    
if __name__ == '__main__':
    AMajor, AMinor, BMinor, CMajor, DMajor, DMinor, EMajor, EMinor, FMajor, GMajor, TestChord= getData()
    
    
    AChroma = addClassification(cleanUpChroma(getChroma(AMajor, 1)),1)
    AMChroma = addClassification(cleanUpChroma(getChroma(AMinor, 2)),2)
    BMChroma = addClassification(cleanUpChroma(getChroma(BMinor, 3)),3)
    CChroma = addClassification(cleanUpChroma(getChroma(CMajor, 4)),4)
    DChroma = addClassification(cleanUpChroma(getChroma(DMajor, 5)),5)
    DMChroma = addClassification(cleanUpChroma(getChroma(DMinor, 6)),6)
    EChroma = addClassification(cleanUpChroma(getChroma(EMajor, 7)),7)
    EMChroma = addClassification(cleanUpChroma(getChroma(EMinor, 8)),8)
    FChroma = addClassification(cleanUpChroma(getChroma(FMajor, 9)),9)
    GChroma = addClassification(cleanUpChroma(getChroma(GMajor, 10)),10)
    #TestChroma1 = addClassification(cleanUpChroma(getChroma([TestChord[0][:]], 8)),0)
    #TestChroma2 = addClassification(cleanUpChroma(getChroma([TestChord[1][:]], 8)),0)
    #TestChroma3 = addClassification(cleanUpChroma(getChroma([TestChord[2][:]], 8)),0)

    
        
    
    '''Concatenating All Matrices Together
       From Above to Create One Data Set'''
    
    totalData = np.concatenate((np.array(AChroma), np.array(AMChroma)))
    totalData = np.concatenate((totalData, np.array(BMChroma)))
    totalData = np.concatenate((totalData, np.array(CChroma)))
    totalData = np.concatenate((totalData, np.array(DChroma)))
    totalData = np.concatenate((totalData, np.array(DMChroma)))
    totalData = np.concatenate((totalData, np.array(EChroma)))
    totalData = np.concatenate((totalData, np.array(EMChroma)))
    totalData = np.concatenate((totalData, np.array(FChroma)))
    totalData = np.concatenate((totalData, np.array(GChroma)))
    np.random.shuffle(totalData)



    
    
    '''Train Network'''

    
    neuralNetwork = batchTraining(AChroma, AMChroma, BMChroma, CChroma, DChroma, DMChroma, EChroma, EMChroma, FChroma, GChroma)
    neuralNetwork = trainNetwork(totalData, neuralNetwork)
    '''

    print("Weights")
    print(neuralNetwork.getWeights())
    print("Biases")
    print(neuralNetwork.getBiases())
    print("Hidden Weights")
    print(neuralNetwork.getHiddenWeights())
    print("Hidden Biases")
    print(neuralNetwork.getHiddenBiases())
    '''
    
