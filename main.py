from func.data import *
from func.utils import *
import numpy as np
from matplotlib import pyplot as plt
# import random


def main():
    # get distance matrix

    DMAT = getMatrixFromCSV("./work_matrix.csv", 1, range(1,50), float)
    # print(DMAT)
    location_num = 48
    break_points = [5, 10 ,15, 20, 25, 30 ,35, 40, 44]
    population_scale = 60
    population = init_population(location_num, population_scale)
    iteration_num = 1000  # set interation_times
    superior_value_record = []
    superior_entity_record = None
    break_points_plt = [0, 5, 10 ,15, 20, 25, 30 ,35, 40, 44, 49]
    for i in range(iteration_num+1):
        print("generation_{}th)".format(i))
        fitness_values = population_fitness(population, DMAT, break_points, aimFunction)
        population_new = selection(population, fitness_values)
        offspring = crossover(population_new, 0.60)
        population = mutation(offspring, 0.12)
        fitness_values = []
        for j in range(population_scale):
            fitness_values.append(1.0/aimFunction(population[j], DMAT, break_points))
        superior_value_record.append(min(fitness_values))
        superior_entity_record = (population[fitness_values.index(min(fitness_values))])
        if i % 20 == 0:
            routes = []
            for j in range(len(break_points_plt)-1):
                routes.append(superior_entity_record[break_points_plt[j]:break_points_plt[j+1]])
            for route in routes:
                while 0 in route:
                    route.remove(0)
                route.insert(0, 0)
                route.append(0)
                print(route)
            print(min(superior_value_record))
        
    # print(population)
        
    


if __name__ == '__main__':
    main()