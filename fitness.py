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

IntervalScore = [0, -5, -3, 0, 0, 0, -2, 0, -1, 0, -3, -5]

ToneScore = [0, -1, 0, -0.7, 0, 0, -1, 0, -0.7, 0, -1, 0]

HeadScore = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
TailScore = [3, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]

chords = [(4,3), (3,5), (5,4), (3,4), (4,5), (5,3)]

def fitness_pitch_chord(melody_code):
    score = 0
    N = len(melody_code)
    delta = [melody_code[i] - melody_code[i-1] for i in range(1,N)]
    for i in range(N):
        if melody_code[i] == 0 or melody_code[i] == 28: 
            if i < N-1: delta[i] = -100
            if i > 0: delta[i-1] = -100

    score += IntervalScore[abs(delta[0] % 12)]
    for i in range(1,N-1):
        score += IntervalScore[abs(delta[i] % 12)]
        if delta[i] > 0 and delta[i-1] > 0 and (delta[i-1], delta[i]) in chords: score += 2
        if delta[i] < 0 and delta[i-1] < 0 and (-delta[i-1], -delta[i]) in chords: score += 2
        if abs(delta[i-1]) > 7 and abs(delta[i] > 5): score -= 10

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
        score -= 100
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

def fitness_rhythm(melody_code):
    N = len(melody_code)
    score = 0
    rhythm_type = [] # 0 休止 1 延长 -1 其他

    cnt_pause, cnt_extend = 0, 0
    for i in range(N):
        if melody_code[i] == 0: rhythm_type.append(0); cnt_pause += 1
        elif melody_code[i] == 28: rhythm_type.append(1); cnt_extend += 1
        else: rhythm_type.append(-1)

    if cnt_pause > 3: score -= (cnt_pause - 3) * 2
    elif cnt_pause <= 1: score -= 5
    if cnt_extend > 4: score -= (cnt_extend - 4) * 2
    elif cnt_extend <= 1: score -= 5

    for i in range(N):
        if rhythm_type[i] >= 0 and i % 4 == 0: 
            score -= 2
        if i % 4 == 3 and i > 3:
            bonus = 0
            for j in range(4):
                if rhythm_type[i-j] != rhythm_type[i-j-4]: bonus = 0; break
                if rhythm_type[i-j] >= 0: bonus = 1
            score += bonus
        if i > 0 and rhythm_type[i] == '-' and rhythm_type[i-1] == '0':
            score -= 1e6
        if rhythm_type[i] == '-' and (i == N-1 or rhythm_type[i+1] != '-'):
            j = i
            while j >= 0 and rhythm_type[j] == '-': j -= 1
            if i-j > 3: score -= 2
            elif i-j == 2 and j % 2 != 0: score -= 2

    return score


def fitness(melody, tone=8):
    melody_code = [Encoding[note] for note in melody]
    fitness_score = fitness_pitch_chord(melody_code) * 3
    fitness_score += fitness_special_cases(melody_code, tone) 
    fitness_score += fitness_tone(melody_code, tone) * 10
    fitness_score += fitness_sequence(melody_code) 
    fitness_score += fitness_rhythm(melody_code) 

    return fitness_score

