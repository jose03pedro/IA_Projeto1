import random
import math
from problem import Problem
from score import Score
from genetic import GeneticAlgorithm

class Algorithms:
    @staticmethod
    def hill_climbing(problem, max_iterations=1000000, log=False):
        current = problem.initial_state()
        current_score = Score.evaluate(problem, current)
        for _ in range(max_iterations):
            neighbors = problem.get_neighbors(current)
            if not neighbors:
                break
            neighbor = max(neighbors, key=lambda state: Score.evaluate(problem, state))
            neighbor_score = Score.evaluate(problem, neighbor)
            if neighbor_score >= current_score:
                current, current_score = neighbor, neighbor_score
        return current

    @staticmethod
    def tabu_search(problem, max_iter=1000000, tabu_size=100):
        current = problem.initial_state()
        best = current
        tabu_list = []

        for i in range(max_iter):
            neighbors = problem.get_neighbors(current)
            neighbors = [n for n in neighbors if n not in tabu_list]

            if not neighbors:
                break
            neighbor = max(neighbors, key=lambda state: Score.evaluate(problem, state))
            current = neighbor
            tabu_list.append(neighbor)

            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            if Score.evaluate(problem, neighbor) > Score.evaluate(problem, best):
                best = neighbor

        return best
    
    @staticmethod
    def genetic_algorithm_tournament(problem, max_iter=1000, mutation_rate=0.01, crossover_func=GeneticAlgorithm.crossover, mutation_func=GeneticAlgorithm.mutation):
        n = len(problem.ingredients)
        population = [[random.choice([True, False]) for _ in range(n)] for _ in range(10)]

        best_solution = population[0] # Initial solution
        best_score = Score.evaluate_bool(problem, best_solution) # Initial score
        best_solution_generation = 0 # Generation on which the best solution was found
        
        generation_no = 0

        no_improvement = 0
        
        while(max_iter > 0):
            new_population = []
            generation_no += 1

            tournment_winner_1 = GeneticAlgorithm.tournament_selection(problem, 4, population)
            tournment_winner_2 = GeneticAlgorithm.tournament_selection(problem, 4, population)

            # Crossover
            child_1 = crossover_func(tournment_winner_1, tournment_winner_2)
            child_2 = crossover_func(tournment_winner_2, tournment_winner_1)

            # Mutation

            child_1 = mutation_func(child_1, mutation_rate)
            child_2 = mutation_func(child_2, mutation_rate)

            # Substituting the worst solution in the population
            new_population = GeneticAlgorithm.substitute_worst(problem, population, child_1)
            new_population = GeneticAlgorithm.substitute_worst(problem, population, child_2)

            population = new_population
            
            # Checking the greatest fit among the current population
            greatest_fit, greatest_fit_score = GeneticAlgorithm.get_greatest_fit(problem, population)
            if greatest_fit_score > best_score:
                best_solution = greatest_fit
                best_score = greatest_fit_score
                best_solution_generation = generation_no
                no_improvement = 0
            else:
                no_improvement += 1
                if no_improvement >= 100:
                    break
            max_iter -= 1
        
        return best_solution
    
    @staticmethod
    def genetic_algorithm_roulette_wheel(problem, max_iter=1000, mutation_rate=0.01, crossover_func=GeneticAlgorithm.crossover, mutation_func=GeneticAlgorithm.mutation):
        n = len(problem.ingredients)
        population = [[random.choice([True, False]) for _ in range(n)] for _ in range(10)]

        best_solution = population[0] # Initial solution
        best_score = Score.evaluate_bool(problem, best_solution) # Initial score
        best_solution_generation = 0 # Generation on which the best solution was found
        
        generation_no = 0

        no_improvement = 0
        
        while(max_iter > 0):
            new_population = []
            generation_no += 1

            fitness = [Score.evaluate_bool(problem, individual) for individual in population]
            tournment_winner_1 = GeneticAlgorithm.roulette_wheel_selection(population, fitness)
            tournment_winner_2 = GeneticAlgorithm.roulette_wheel_selection(population, fitness)

            # Crossover
            child_1 = crossover_func(tournment_winner_1, tournment_winner_2)
            child_2 = crossover_func(tournment_winner_2, tournment_winner_1)

            # Mutation

            child_1 = mutation_func(child_1, mutation_rate)
            child_2 = mutation_func(child_2, mutation_rate)

            # Substituting the worst solution in the population
            new_population = GeneticAlgorithm.substitute_worst(problem, population, child_1)
            new_population = GeneticAlgorithm.substitute_worst(problem, population, child_2)

            population = new_population
            
            # Checking the greatest fit among the current population
            greatest_fit, greatest_fit_score = GeneticAlgorithm.get_greatest_fit(problem, population)
            if greatest_fit_score > best_score:
                best_solution = greatest_fit
                best_score = greatest_fit_score
                best_solution_generation = generation_no
                no_improvement = 0
            else:
                no_improvement += 1
                if no_improvement >= 100:
                    break
            max_iter -= 1
        
        return best_solution
    
    @staticmethod
    def genetic_algorithm_fitness(problem, max_iter=1000, mutation_rate=0.01):
        n = len(problem.ingredients)
        population = [[random.choice([True, False]) for _ in range(n)] for _ in range(10)]
        fitness = [Problem.evaluate(problem, problem.get_list_ingredients_true(individual)) for individual in population]
        best_fitness = -1
        while max_iter >0:
            new_population = []
            p1, p2 = GeneticAlgorithm.select_parents(population, fitness)
            c1 = GeneticAlgorithm.crossover(p1, p2)
            c2 = GeneticAlgorithm.crossover(p2, p1)
            c1 = GeneticAlgorithm.mutation(c1, mutation_rate)
            c2 = GeneticAlgorithm.mutation(c2, mutation_rate)
            new_population = GeneticAlgorithm.substitute_worst(problem, population, c1)
            new_population = GeneticAlgorithm.substitute_worst(problem, population, c2)
            population = new_population
            fitness = [Problem.evaluate(problem, problem.get_list_ingredients_true(individual)) for individual in population]
            if max(fitness) > best_fitness:
                best_fitness = max(fitness)
            max_iter -= 1
        return max(population, key=lambda individual: Score.evaluate(problem, individual))
    
    @staticmethod
    def simulated_annealing(problem, max_iter=10000, temperature=1000):
        current = [False for _ in range(len(problem.ingredients))]
        current_score = Score.evaluate_bool(problem, current)
        best = current
        best_score = current_score
        reheat_iter = 2000
        reheat_factor = 1.1
        for i in range(max_iter):
            temperature = temperature * 0.999
            if i % reheat_iter == 0:
                temperature *= reheat_factor
            if temperature == 0:
                break
            neighbour = problem.get_neighbours_bool(current)
            neighbour_score = Score.evaluate_bool(problem, neighbour)
            diff = neighbour_score - current_score
        
            if(diff > 0 or math.exp(diff/temperature) > random.random()):
                current = neighbour
                current_score = neighbour_score
                if current_score > best_score:
                    best = current
                    best_score = current_score
        return best