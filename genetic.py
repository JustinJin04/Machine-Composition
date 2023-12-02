import random
import numpy as np
from fitness import fitness
from crossover import crossover
from mutate import mutate

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

# 将分数归一化，变换为目标的标准差
def normalize_weights(scores, std_before_exp=1.):
    print(scores)
    mean, std = np.mean(scores), np.std(scores)
    if std < 1e-3: return [1.] * len(scores)
    scores = (scores - mean) / std * std_before_exp
    weights = np.exp(scores)
    print(weights)
    return weights


# 遗传算法迭代
def genetic_algorithm(pop_size=10, 
                      melody_length=8, 
                      generations=50,
                      mutate_rate=0.2,
                      ):
    population = generate_population(pop_size, melody_length)

    for generation in range(generations):
        # 计算适应度
        fitness_scores = [fitness(melody) for melody in population]

        # 输出当前代的最佳旋律
        best_melody = population[fitness_scores.index(max(fitness_scores))]
        #encody_melody = [Encoding[note] for note in best_melody]
        print(f"Fitness: {fitness_scores}")
        print(f"Generation {generation + 1}, Best Melody: {best_melody}, Best Fitness: {max(fitness_scores)}")

        # 将分数归一化
        choice_weights = normalize_weights(fitness_scores)

        # 选择父代
        parents = random.choices(population, weights=choice_weights, k=pop_size*2)

        # 生成子代
        offspring = []
        for i in range(pop_size):

            parent1, parent2 = parents[i*2], parents[i*2+1]
            child = crossover(parent1, parent2)

            if random.uniform(0, 1) < mutate_rate:
                child = mutate(child)
            
            offspring.append(child)

        # 更新种群
        population = offspring

    return best_melody

