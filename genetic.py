import random

# 定义音符体系
melody_system = ['0','F3','#F3','G3','#G3','A3','#A3','B3','C4', '#C4','D4','#D4','E4',
                 'F4','#F4','G4','#G4','A4','#A4','B4','C5', '#C5','D5','#D5','E5',
                 'F5','#F5','G5','-']

# 生成初始种群
def generate_population(pop_size, melody_length):
    population = []
    for _ in range(pop_size):
        melody = [random.choice(melody_system) for _ in range(melody_length)]
        population.append(melody)
    return population

# 自适应度函数
def fitness(melody):
    fitness_score = random.randint(1, 100)
    return fitness_score

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

