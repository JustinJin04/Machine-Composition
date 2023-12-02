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

IntervalScore = [0, -5, -3,  0,  0,  0, -2,  0,  -1,  0, -3, -5]

ToneScore =     [1,  0,  1,0.3,  1,  1,  0,  1, 0.3,  1,  0,  1]

HeadScore =     [1,  0,  0,  0,  1,  0,  0,  1,   0,  0,  0,  0]
TailScore =     [2,  0,  0,  0,  1,  0,  0,  1,   0,  0,  0,  0]

def fitness_pitch(melody_code):
    score = 0
    i = 0
    if melody_code[i] == 28 or melody_code[i] == 0: i += 1
    j = i + 1
    length = len(melody_code)
    while j < length:
        if melody_code[j] == 28 or melody_code[j] == 0:
            j += 1
            continue
        delta = abs(melody_code[i] - melody_code[j])
        score += IntervalScore[delta % 12]
        
        if delta > 11: score -= 2
        i = j
        j += 1
    return score

def fitness_tone(melody_code, tone=8):
    score = 0
    for i in melody_code:
        if i == 28 or i == 0: score += 0.5
        else: score += ToneScore[(i - tone) % 12]
    return score

def fitness_special_cases(melody_code, tone=8):
    score = 0
    if melody_code[0] in [0, 28]: 
        score -= 10
    else: 
        score += HeadScore[(melody_code[0] - tone) % 12]

    # please add
    if melody_code[-1] not in [0, 28]:
        score += TailScore[(melody_code[-1] - tone) % 12]

    return score

def fitness_sequence(melody_code):
    N = len(melody_code)
    score = 0
    for i in range(0, N, 4):
        if melody_code[i] < melody_code[i+1] and melody_code[i+1] < melody_code[i+2] \
            and melody_code[i+2] < melody_code[i+3] and melody_code[i] > 0 and melody_code[i+3] < 28: score += 1
        elif melody_code[i] > melody_code[i+1] and melody_code[i+1] > melody_code[i+2] \
            and melody_code[i+2] > melody_code[i+3] and melody_code[i+3] > 0 and melody_code[i] < 28: score += 1
        
    for i in range(2, N):
        if melody_code[i] == melody_code[i-2] and melody_code[i] == melody_code[i-1]: score -= 1
    return score


def fitness(melody, tone=9):
    melody_code = [Encoding[note] for note in melody]
    fitness_score = fitness_pitch(melody_code) * 4
    fitness_score += fitness_special_cases(melody_code, tone) * 10
    fitness_score += fitness_tone(melody_code, tone) * 10
    fitness_score += fitness_sequence(melody_code) * 3
    return fitness_score

