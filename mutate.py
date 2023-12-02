import random

# 变异操作
melody_system = ['0','F3','#F3','G3','#G3','A3','#A3','B3','C4', '#C4','D4','#D4','E4',
                 'F4','#F4','G4','#G4','A4','#A4','B4','C5', '#C5','D5','#D5','E5',
                 'F5','#F5','G5','-']

# 以 p 的概率把延长和两个相同的音相互转化
def mutate_extend(melody, p=0.3):
    for i in range(1, len(melody)):
        if melody[i] == melody[i-1] and random.uniform(0, 1) < p:
            melody[i] = '-'
        elif melody[i] == '-' and random.uniform(0, 1) < p:
            melody[i] = melody[i-1]
    return melody
            

def mutate(melody):
    mutation_point = random.randint(0, len(melody) - 1)
    melody[mutation_point] = random.choice(melody_system)
    return melody
