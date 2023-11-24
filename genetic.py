import random

# 定义音符体系
melody_system = ['F3', '#F3', 'B3', 'C4', '#C4', 'B4', 'C5', '#C5', '#F5', 'G5']

# 生成初始种群
def generate_population(pop_size, melody_length):
    population = []
    for _ in range(pop_size):
        melody = [random.choice(melody_system) for _ in range(melody_length)]
        population.append(melody)
    return population\
    
# 自适应度函数

def fitness(melody):
    # 适应度的初始值
    fitness_score = 0.0
    
    # 1. 音高连续性
    pitch_changes = sum(1 for i in range(1, len(melody)) if melody[i] != melody[i - 1])
    fitness_score += 1.0 / (1.0 + pitch_changes)
    
    return fitness_score
'''
def fitness(melody):
    return random.uniform(0, 1)
'''

# 交叉操作
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# 变异操作
def mutate(melody):
    mutation_point = random.randint(0, len(melody) - 1)
    melody[mutation_point] = random.choice(melody_system)
    return melody

# 遗传算法迭代
def genetic_algorithm(pop_size, melody_length, generations):
    population = generate_population(pop_size, melody_length)

    for generation in range(generations):
        # 计算适应度
        fitness_scores = [fitness(melody) for melody in population]

        # 选择父代
        parents = random.choices(population, weights=fitness_scores, k=pop_size)

        # 生成子代
        offspring = []
        for i in range(0, pop_size, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            offspring.extend([mutate(child1), mutate(child2)])

        # 更新种群
        population = offspring

        # 输出当前代的最佳旋律
        best_melody = population[fitness_scores.index(max(fitness_scores))]
        print(f"Generation {generation + 1}, Best Melody: {best_melody}, Fitness: {max(fitness_scores)}")
    
    return best_melody

