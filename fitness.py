import random
import math

Encoding = {
    '0':0,
    'F3':1,'#F3':2,'G3':3,'#G3':4,'A3':5,'#A3':6,'B3':7,'C4':8,'#C4':9,'D4':10,'#D4':11,'E4':12,
    'F4':13,'#F4':14,'G4':15,'#G4':16,'A4':17,'#A4':18,'B4':19,'C5':20, '#C5':21,'D5':22,'#D5':23,'E5':24,
    'F5':25,'#F5':26,'G5':27,
    '-':28
}

Decoding = {
    0:'0',
    1:'F3',2:'#F3',3:'G3',4:'#G3',5:'A3',6:'#A3',7:'B3',8:'C4',9:'#C4',10:'D4',11:'#D4',12:'E4',
    13:'F4',14:'#F4',15:'G4',16:'#G4',17:'A4',18:'#A4',19:'B4',20:'C5',21:'#C5',22:'D5',23:'#D5',24:'E5',
    25:'F5',26:'#F5',27:'G5',
    28:'-'
}

IntervalScore=[0,-3,-2,0,0,0,-2,0,-1,0,-1,-3]

def fitness_pitch(melody_code):
    fitness_score = 0
    i=0
    if melody_code[i]==28 or melody_code[i]==0:
        i+=1
    j=i+1
    length=len(melody_code)
    while j<length:
        if melody_code[j]==28 or melody_code[j]==0:
            j+=1
            continue
        fitness_score+=IntervalScore[abs(melody_code[i]-melody_code[j])%12]
        i=j
        j+=1
    return fitness_score


def fitness(melody):
    fitness_score = 10
    melody_code=[Encoding[note] for note in melody]
    fitness_score+=fitness_pitch(melody_code)
    return fitness_score

