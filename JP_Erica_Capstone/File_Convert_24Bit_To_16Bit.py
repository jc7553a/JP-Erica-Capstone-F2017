import soundfile
import os


path = 'C:\JP_Erica_Capstone\JP_Erica_Capstone\Data\BChord'
num = 1
i = 1
for filename in os.listdir(path):
    data, samplerate = soundfile.read(filename)
    soundfile.write('BMajor_'+str(i)+'_'+str((num%2))+'_1.wav', data, samplerate, subtype='PCM_16')
    if num%2 == 0:
        i +=1
    num+=1
#'AMajor_'+str(i)+ '_'+str((num%2)+1)+'_1.wav'
