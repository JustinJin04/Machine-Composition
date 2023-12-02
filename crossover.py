import random
from fitness import fitness

# 定义音符体系
melody_system = ['0','F3','#F3','G3','#G3','A3','#A3','B3','C4', '#C4','D4','#D4','E4',
                 'F4','#F4','G4','#G4','A4','#A4','B4','C5', '#C5','D5','#D5','E5',
                 'F5','#F5','G5','-']

# 交叉操作总函数
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child