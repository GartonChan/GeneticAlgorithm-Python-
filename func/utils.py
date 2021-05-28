import numpy as np
import copy
import random

def code(length):
    # return a random sequence as a entity
    entity_seq = [i for i in range(1, length+1)]
    random.shuffle(entity_seq)
    # print(entity_seq)
    return entity_seq

def init_population(length, population_scale):
    # generate a initial population
    population = []
    for i in range(population_scale):
        population.append(code(length))
    return population

def decode(entity, break_points):
    # decode: convert the entity gene code to routes
    routes = []
    for i in range(len(break_points) - 1):
        routes.append(entity[break_points[i]: break_points[i+1]])
    # print(routes)
    return routes

def aimFunction(entity, DMAT, break_points):
    # catculate the fitness of entity through self-defined aimFunction
    distance = 0
    break_points.insert(0, 0)
    break_points.append(len(entity))
    routes = decode(entity, break_points)
    for route in routes:
        while 0 in route:
            route.remove(0)
        route.insert(0, 0)
        route.append(0)
        for i in range(len(route) - 1):
            distance += DMAT[route[i], route[i+1]]
    if distance != 0:
        return 1.0 / distance
    else:
        return distance

def population_fitness(population, DMAT, break_points, aimFunction):
    fitness_values = []
    for i in range(len(population)):
        fitness_values.append(aimFunction(population[i], DMAT, copy.deepcopy(break_points)))
        if fitness_values[i] < 0:
            fitness_values[i] = 0
    return fitness_values

# 这里的轮盘赌与蚁群算法的有一定区别。这里对适应度归一化得到概率之后，每个个体被选中的概率就是这个概率
# 对每次被选中的个体的数目没有限制，完全随机，限制的是选择次数n与种群数目相同，使得新的种群数量与旧的种群一致
def selection(population, fitness_values):
    # 轮盘赌选择
    fitness_sum = []
    for i in range(len(fitness_values)):
        if i == 0:
            fitness_sum.append(fitness_values[i])
        else:
            fitness_sum.append(fitness_sum[i-1] + fitness_values[i])
    fitness_sum = np.array(fitness_sum)
    fitness_sum /= sum(fitness_values)
    # select new population
    population_new = []
    for i in range(len(fitness_values)):
        rand = np.random.uniform(0, 1)  
        # 选择rand对应的fitness_values的一个区间
        for j in range(len(fitness_values)):
            if j == 0:
                if 0 < rand and rand <= fitness_sum[j]:
                    population_new.append(population[j])
            else:
                if fitness_sum[j-1] < rand and rand <= fitness_sum[j]:
                    population_new.append(population[j])
    return population_new

def amend(entity, low, high):
    # 修正交叉个体，对非交叉片段基因进行修正，以保证基因序列完备性
    length = len(entity)
    cross_gene = entity[low:high]  # 个体交叉片段的基因
    raw = entity[0:low] + entity[high: ]  # 个体非交叉片段的基因

    not_in_cross = [] # 非交叉片段应含有的基因集合
    for i in range(1, length+1):  
        if not i in cross_gene:
            not_in_cross.append(i)

    error_index = []  
    # 扫描非交叉片段中的错误基因位点
    for i in range(len(raw)):
        if raw[i] in not_in_cross:  # 当前基因正确
            not_in_cross.remove(raw[i])
        else:  # 当前基因出错
            error_index.append(i)
    # 根据位点结合not_in_cross进行修正
    for i in range(len(error_index)):
        raw[error_index[i]] = not_in_cross[i]
    amend_entity = raw[0:low] + cross_gene + raw[low: ]
    return amend_entity

def crossover(population_new, pc):
    half = int(len(population_new)//2)
    father = population_new[ :half]  # 前半种群的个体为父亲
    mother = population_new[half: ]  # 后半种群的个体为母亲
    # 打乱
    np.random.shuffle(father)
    np.random.shuffle(mother)
    # 两两交叉生成一子一女，产生后代种群
    offspring = []
    for i in range(half):
        if np.random.uniform(0, 1) <= pc: # 交叉
            # [cur1, cut2]为交叉区间
            cut1 = 0
            cut2 = np.random.randint(0, len(population_new[0]))
            # if cut1 > cut2:
            #     cut1, cut2 = cut2, cut1
            if cut1 == cut2:  # 区间为空集时，直接克隆父亲，母亲作为子女个体
                son = father[i]
                daughter = mother[i]
            else:
                son = father[i][0:cut1] + mother[i][cut1:cut2] + father[cut2: ]
                daughter = mother[i][0:cut1] + father[i][cut1:cut2] + mother[i][cut2: ]
                # 修正基因信息
                son = amend(son, cut1, cut2)
                son = amend(daughter, cut1, cut2)
        else:  # 不发生交叉，直接克隆父母
            son = father[i]
            daughter = mother[i]
        offspring.append(son)
        offspring.append(daughter)
    return offspring


def mutation(offspring, pm):
    # directly swap two gene in the gene sequence as the simplest mutation
    for i in range(len(offspring)):
        if np.random.uniform(0, 1) <= pm:
            position1 = np.random.randint(0, len(offspring[0]))
            position2 = np.random.randint(0, len(offspring[0]))
            offspring[i][position1], offspring[i][position2] = \
                offspring[i][position2], offspring[i][position1]
    return offspring
