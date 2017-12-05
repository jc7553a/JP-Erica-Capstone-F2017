import numpy as np
import math
import HPCP as HPCP
import os
import sys, json


'''Our Neural Network HardCoded'''

myValues = { "Weights" : [[  1.33877695,   2.42611885,  -1.6498524,    7.76013899,   0.77143258,
       -3.57863641, -10.41831493,   2.58790898,   2.19516683],
     [ -3.04577971,  -2.60280824,  -1.73133159,  -2.58085465,  -3.33878398,
        5.49133348,  10.37589455,  -3.32649541,  -3.88968325],
     [ -2.99838901,   1.13549161,  -7.24953842, -10.32991505,  -3.87962413,
      -12.81757641,   7.27493429,   2.22906208,  18.84435844],
     [ -3.960428,    -2.64069605,  -4.6558814,   -0.80620283,  -4.09178162,
       -7.22601604,   7.41209221,  -0.73860425,  -6.28695917],
     [ -6.08905315,  -3.24493837,  -6.38586378,  -0.72087651,  -6.53085709,
       -8.1195097,    2.45569777,  -0.45266038,  -2.60400534],
     [ -3.07358646,  -3.13332224,  -1.37454772,   9.08749104,  -2.75056839,
       -1.02353573, -13.40280342,  -3.36011529,  -3.52689719],
     [  1.85643816,   3.7503438,   -2.07958126,   0.91555011,   2.46813178,
       -4.68322325,  -3.29586363,   5.91936541,   5.27369642],
     [  0.80757564,  -0.75285047,   1.29191494,   2.20938015,   0.32239756,
       -3.66530895,  -0.37317574,  -1.79141235,   2.03516078],
     [ -2.3198545,   -1.63475239,  -2.99360085,   5.4830265,   -2.34922004,
       -3.71514416, -13.31292725,  -1.91707003,   4.93871689],
     [ -4.36809301,  -3.71500564,   2.53857374,   4.45831919,  -6.51977396,
        1.73498857, -27.43795776,  -7.5555377,    1.10429311],
     [ -2.66566992,  -2.46926045,  -2.35029268,   2.64521575,  -2.78282809,
       -3.20256853,   3.07838535,  -2.00939775,  -9.31940842],
     [ -8.90785599,  -8.21330547,  -8.68538666,   1.83948112, -10.51830959,
      -16.28369331,  -0.3287681,   -9.55752659,   0.91085398]],

    "Biases": [-2.80140018, -5.25328827, -1.32360482, -9.0696249,  -2.18938375,  3.57379103,
     -0.27621222, -5.23886108, -4.83810806],

    "hiddenWeights": [[ 3.77329278],
     [ 2.41901088],
     [ 4.0241046 ],
     [ 4.59296274],
     [ 4.60128307],
     [ 1.67480576],
     [ 3.7662282 ],
     [ 2.9760673 ],
     [ 2.80536699]],

    "hiddenBias" :[ 1.27858722]}


'''Our Activation Function For Neural Network'''

def sigmoid(x):
    return 1/(1+math.exp(-x))

'''Get's Wav File From Path'''

def getData():
    path8 = 'C:/JP_Erica_Capstone/JP_Erica_Capstone/node-app/Chord-Recognition/Data/Uploads'
    TestSong = []
    for filename in os.listdir(path8):
        holder = []
        holder.append(filename)
        holder.append([1])
        TestSong.append(holder)
    return TestSong

'''Gets Harmonic Pitch Class Profile'''
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

'''Pointless Function but let it be'''
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


'''Runs our HPCP Through the Neural Network'''
def testNetwork(testingDataGiven):
    global myValues
    values = []
    for i in range(len(testingDataGiven)):
        vector = testingDataGiven[i][0:12]
        hidden = np.add(np.matmul(vector, myValues.get("Weights")), myValues.get("Biases"))
        for i in range (len(hidden)):
            hidden[i] = sigmoid(hidden[i])
        output = (np.add(np.matmul(hidden, myValues.get("hiddenWeights")), myValues.get("hiddenBias")))
        values.append(output)
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
        #elif values[i] > 7.8:
         #   threshedValues.append(8)
    return threshedValues


'''Find Index that has Max Value in Array'''
def findMaxIndex(listGiven):
    maxNum = 0
    maxIndex = 0
    for j in range(len(listGiven)):
        if listGiven[j] > maxNum:
            maxNum = listGiven[j]
            maxIndex = j
    return maxIndex

'''Finds Which Chord Occurs Most Frequently'''
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
    majorityLeader = findMaxIndex(myArray)
    return majorityLeader+1

'''Converts Number Found in Find Majority to a Chord Letter'''
def numberToChord(number):
    if number == 1:
        return "A"
    elif number == 2:
        return "B"
    elif number == 3:
        return "C"
    elif number == 4:
        return "D"
    elif number == 5:
        return "E"
    elif number == 6:
        return "F"
    elif number == 7:
        return "G"


def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])


if __name__ == '__main__':
    lines = read_in()
    lineString= ""
    for l in lines:
        lineString +=str(l)
    ''' Get Data'''
    
    TestChord= getData()
    #print(TestChord)
    TestChroma1 = addClassification(cleanUpChroma(getChroma([TestChord[0][:]], 11)),0)
    '''Run it Through Harmonic Pitch Class Profile'''


    '''Run it Through Neural Network'''
    predictedValues = testNetwork(TestChroma1)

    '''Checking the Results'''
    '''Hacky Check If it's longer than 700 than chances are it's multiple Chords'''
    '''The Smaller the Length prob means it's a single Chord'''
    
    time = []
    correctValues = []
    if len(TestChroma1) > 500:
        i = 0
        chordChange = 0
        chord = 0
        while i < (len(predictedValues)-35):
            chordChange = 0
            if i ==0:
                chord = findMajority(predictedValues[i:i+20])
                chordChange = 1
            else:
                temp = findMajority(predictedValues[i-10:i+35])
                if chord != temp:
                    chord = temp
                    chordChange = 1
            if chordChange ==1:
                if chord == 1:
                    correctValues.append("A")
                if chord == 2:
                    correctValues.append("B")
                if chord == 3:
                    correctValues.append("C")
                if chord == 4:
                    correctValues.append("D")
                if chord == 5:
                    correctValues.append("E")
                if chord == 6:
                    correctValues.append("F")
                if chord == 7:
                    correctValues.append("G")
                time.append(round((i+35)/45.0,2))
            chordChange = 0
            i+=35
    else:
        correctValues.append(numberToChord(findMajority(predictedValues)))
        time.append(0)
    time[0] = 0
    
    print([str(correctValues) + str(time) + lineString])
