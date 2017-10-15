import numpy as np
import HPCP as HPCP
import MLP as net
import random as ra
import math
import tensorflow as tf
import os
import matplotlib.pylab as plt
from random import randint
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve


def getData():
    path = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/BChord'
    path2 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/BChord'
    path3 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/CChord'
    path4 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/DChord'
    path5 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/EChord'
    path6 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/FChord'
    path7 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/GChord'
    path8 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/TestSong'

    AMajor = []
    TestSong = []
    for filename in os.listdir(path):
        holder = []
        holder.append(filename)
        holder.append([1])
        AMajor.append(holder)
        
    BMajor = []
    for filename in os.listdir(path2):
        holder = []
        holder.append(filename)
        holder.append([1])
        BMajor.append(holder)

    CMajor = []
    for filename in os.listdir(path3):
        holder = []
        holder.append(filename)
        holder.append([1])
        CMajor.append(holder)

    DMajor = []
    for filename in os.listdir(path4):
        holder = []
        holder.append(filename)
        holder.append([2])
        DMajor.append(holder)

    EMajor = []
    for filename in os.listdir(path5):
        holder = []
        holder.append(filename)
        holder.append([1])
        EMajor.append(holder)

    FMajor = []
    for filename in os.listdir(path6):
        holder = []
        holder.append(filename)
        holder.append([1])
        FMajor.append(holder)

    GMajor = []
    for filename in os.listdir(path7):
        holder = []
        holder.append(filename)
        holder.append([3])
        GMajor.append(holder)
    
    TestSong = []
    for filename in os.listdir(path8):
        holder = []
        holder.append(filename)
        holder.append([1])
        TestSong.append(holder)
        
    return AMajor, BMajor, CMajor, DMajor, EMajor, FMajor, GMajor, TestSong


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
def trainNetwork(data):
    print("Training Network....")
    network = net.MLP(12, 9)
    #np.random.shuffle(data)
    losses = []
    for i in range(5):
        midLosses = []
        for j in range(len(data)):
            rand = randint(0, len(data)-1)
            midLosses.append(network.train([data[rand][0:12]], [[data[rand][12]]]))
        losses.append(np.average(midLosses))
    #plt.plot(losses)
    #plt.show()
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
    

if __name__ == '__main__':
    AMajor, BMajor, CMajor, DMajor, EMajor, FMajor, GMajor, TestChord= getData()
    print(TestChord[1][:])
    
    AChroma = addClassification(cleanUpChroma(getChroma(AMajor, 1)),1)
    BChroma = addClassification(cleanUpChroma(getChroma(BMajor, 2)),2)
    CChroma = addClassification(cleanUpChroma(getChroma(CMajor, 3)),3)
    DChroma = addClassification(cleanUpChroma(getChroma(DMajor, 4)),4)
    EChroma = addClassification(cleanUpChroma(getChroma(EMajor, 5)),5)
    FChroma = addClassification(cleanUpChroma(getChroma(FMajor, 6)),6)
    GChroma = addClassification(cleanUpChroma(getChroma(GMajor, 7)),7)
    TestChroma1 = addClassification(cleanUpChroma(getChroma([TestChord[0][:]], 8)),0)
    TestChroma2 = addClassification(cleanUpChroma(getChroma([TestChord[1][:]], 8)),0)
    #TestChroma3 = addClassification(cleanUpChroma(getChroma([TestChord[2][:]], 8)),0)
    
        
    
    '''Concatenating All Matrices Together
       From Above to Create One Data Set'''
    totalData = np.concatenate((np.array(AChroma), np.array(BChroma)))
    totalData = np.concatenate((totalData, np.array(CChroma)))
    totalData = np.concatenate((totalData, np.array(DChroma)))
    totalData = np.concatenate((totalData, np.array(EChroma)))
    totalData = np.concatenate((totalData, np.array(FChroma)))
    totalData = np.concatenate((totalData, np.array(GChroma)))
    np.random.shuffle(totalData)
    
    '''Choosing Random Samples to Test on
       Then Deleting them from Training'''
    '''
    trainSize = 10000
    testingData = []    
    for i in range(trainSize):
        #rand = randint(0, len(totalData)-1)
        testingData.append(totalData[i][:])
        totalData = np.delete(totalData,(i), axis = 0)
    '''
    #testingData = totalData[0:10000][:]
    #totalData = totalData[10000:len(totalData)-1][:]
    
    
    '''Train Network'''
    neuralNetwork = trainNetwork(totalData)

    '''Test Network'''
    predictedValues = testNetwork(neuralNetwork, TestChroma2)
    

    '''
    ones = 0
    twos= 0
    threes = 0
    fours = 0
    fives = 0
    six = 0
    seven = 0
    for i in range(len(predictedValues)):
        if predictedValues[i] == 1:
            ones +=1
        if predictedValues[i] == 2:
            twos +=1
        if predictedValues[i] == 3:
            threes +=1
        if predictedValues[i] == 4:
            fours +=1
        if predictedValues[i] == 5:
            fives +=1
        if predictedValues[i] == 6:
            six +=1
        if predictedValues[i] == 7:
            seven +=1

    things = []
    things.append(ones)
    things.append(twos)
    things.append(threes)
    things.append(fours)
    things.append(fives)
    things.append(six)
    things.append(seven)
    print(things)
    print(findMaxIndex(things))
    '''

    #print(findMajority(predictedValues))
    
    i = 0
    while i < (len(predictedValues)-50):
        if i ==0:
            chord = 1
            sp = 1
        else:
            temp = findMajority(predictedValues[i:i+50])
            if chord != temp:
                chord = temp
                sp = 1
        if sp ==1:
            if chord == 1:
                print("A")
            if chord == 2:
                print("B")
            if chord == 3:
                print("C")
            if chord == 4:
                print("D")
            if chord == 5:
                print("E")
            if chord == 6:
                print("F")
            if chord == 7:
                print("G")
        sp = 0
        
        i+=50
                             

    #neuralNetwork.saveTensor() 

    '''

    
    falseAChord = 0
    AChordCorrect = 0
    falseBChord = 0
    BChordCorrect = 0
    falseCChord = 0
    CChordCorrect = 0
    falseDChord = 0
    DChordCorrect = 0
    falseEChord = 0
    EChordCorrect = 0
    falseFChord = 0
    FChordCorrect = 0
    falseGChord = 0
    GChordCorrect = 0
    actual = []

    for i in range(len(predictedValues)):
        if predictedValues[i] == 1 and testingData[i][12] == 1:
            AChordCorrect += 1
        elif predictedValues[i] != 1 and testingData[i][12] == 1:
            falseAChord += 1
        elif predictedValues[i] == 2 and testingData[i][12] == 2:
            BChordCorrect += 1
        elif predictedValues[i] != 2 and testingData[i][12] == 2:
            falseBChord +=1
        elif predictedValues[i] == 3 and testingData[i][12] == 3:
            CChordCorrect += 1
        elif predictedValues[i] != 3 and testingData[i][12] == 3:
            falseCChord +=1
        elif predictedValues[i] == 4 and testingData[i][12] == 4:
            DChordCorrect += 1
        elif predictedValues[i] != 4 and testingData[i][12] == 4:
            falseDChord +=1
        elif predictedValues[i] == 5 and testingData[i][12] == 5:
            EChordCorrect += 1
        elif predictedValues[i] != 5 and testingData[i][12] == 5:
            falseEChord +=1
        elif predictedValues[i] == 6 and testingData[i][12] == 6:
            FChordCorrect += 1
        elif predictedValues[i] != 6 and testingData[i][12] == 6:
            falseFChord +=1
        elif predictedValues[i] == 7 and testingData[i][12] == 7:
            GChordCorrect += 1
        elif predictedValues[i] != 7 and testingData[i][12] == 7:
            falseGChord +=1


    print("AChord Tests")
    print(falseAChord)
    print(AChordCorrect)
    print("BChord Tests")
    print(falseBChord)
    print(BChordCorrect)
    print("CChord Tests")
    print(falseCChord)
    print(CChordCorrect)
    print("DChord Tests")
    print(falseDChord)
    print(DChordCorrect)
    print("EChord Tests")
    print(falseEChord)
    print(EChordCorrect)
    print("FChord Tests")
    print(falseFChord)
    print(FChordCorrect)
    print("GChord Tests")
    print(falseGChord)
    print(GChordCorrect)

            
    totalCorrect= AChordCorrect + BChordCorrect + CChordCorrect + DChordCorrect + EChordCorrect + FChordCorrect + GChordCorrect
    total = totalCorrect +(falseAChord + falseBChord + falseCChord+ falseDChord + falseEChord + falseFChord + falseGChord)
    print("")
    print("Accuracy")
    print(float(totalCorrect/total))

    actualValues = []
    for i in range(len(testingData)):
        actualValues.append(testingData[i][12])
    print(testingResults(actualValues, predictedValues))
        
    '''
    print("Weights")
    print(neuralNetwork.getWeights())
    print("Biases")
    print(neuralNetwork.getBiases())
    print("Hidden Weights")
    print(neuralNetwork.getHiddenWeights())
    print("Hidden Biases")
    print(neuralNetwork.getHiddenBiases())
