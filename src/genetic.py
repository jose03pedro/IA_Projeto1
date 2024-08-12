import random
from score import Score
from problem import Problem

class GeneticAlgorithm:
    @staticmethod
    
    def mutation(individual, mutation_rate):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual[i] = not individual[i]
        return individual
    
    def crossover(individual1, individual2):
        n = len(individual1)
        c = random.randint(0, n)
        return individual1[:c] + individual2[c:]
    
    def select_parents(population, fitness):
        n = len(population)
        p1 = random.choices(population, weights=fitness, k=1)[0]
        p2 = random.choices(population, weights=fitness, k=1)[0]
        return p1, p2
    
    def select_children(population, fitness):
        n = len(population)
        c1 = random.choices(population, weights=fitness, k=1)[0]
        c2 = random.choices(population, weights=fitness, k=1)[0]
        return c1, c2
    
    def tournament_selection(problem, tournament_size=5, population=None):
        tournament = random.sample(population, tournament_size)
        best_individual = max(tournament, key=lambda individual: Score.evaluate_bool(problem, individual))
        return best_individual
    
    def get_greatest_fit(problem, population):
        greatest_fit = max(population, key=lambda individual: Score.evaluate_bool(problem, individual))
        greatest_fit_score = Score.evaluate_bool(problem, greatest_fit)
        return greatest_fit, greatest_fit_score
    
    def substitute_worst(problem, population, new_individual):
        worst_individual = min(population, key=lambda individual: Score.evaluate_bool(problem, individual))
        population[population.index(worst_individual)] = new_individual
        return population
    
    def roulette_wheel_selection(population, fitness):
        n = len(population)
        total_fitness = sum(fitness)
        p = random.random()
        s = 0
        for i in range(n):
            s += fitness[i] / total_fitness
            if s >= p:
                return population[i]
        return population[-1]
    
    def genetic_algorithm_random(problem, max_iter=1000000, population_size=100, mutation_rate=0.01):
        n = len(problem.clients)
        population = [[random.choice([True, False]) for _ in range(n)] for _ in range(population_size)]
        fitness = [Score.evaluate(problem, individual) for individual in population]
        for _ in range(max_iter):
            new_population = []
            for _ in range(population_size // 2):
                p1, p2 = GeneticAlgorithm.select_parents(population, fitness)
                c1, c2 = GeneticAlgorithm.crossover(p1, p2)
                c1 = GeneticAlgorithm.mutation(c1, mutation_rate)
                c2 = GeneticAlgorithm.mutation(c2, mutation_rate)
                new_population = GeneticAlgorithm.substitute_worst(problem, new_population, c1)
                new_population = GeneticAlgorithm.substitute_worst(problem, new_population, c2)
            population = new_population
            fitness = [Score.evaluate(problem, individual) for individual in population]
        return max(population, key=lambda individual: Score.evaluate(problem, individual))
    
    def genetic_algorithm_tournament(problem, max_iter=1000000, population_size=100, mutation_rate=0.01, crossover_func=crossover, mutation_func=mutation):
        population = [[random.choice([True, False]) for _ in range(len(problem.clients))] for _ in range(population_size)]

        best_solution = population[0] # Initial solution
        best_score = Score.evaluate(problem, best_solution) # Initial score
        best_solution_generation = 0 # Generation on which the best solution was found
        
        generation_no = 0
        
        print(f"Initial solution: {best_solution}, score: {best_score}")
        
        while(max_iter > 0):
            
            generation_no += 1
            
            tournment_winner_1 = GeneticAlgorithm.tournament_selection(population, 4)
            tournment_winner_2 = GeneticAlgorithm.tournament_selection(population, 4)

            # Crossover
            child_1, child_2 = crossover_func(tournment_winner_1, tournment_winner_2)

            # Mutation

            child_1 = mutation_func(child_1, mutation_rate)
            child_2 = mutation_func(child_2, mutation_rate)

            # Substituting the worst solution in the population
            population = GeneticAlgorithm.substitute_worst(problem, population, child_1)
            population = GeneticAlgorithm.substitute_worst(problem, population, child_2)
            
            # Checking the greatest fit among the current population
            greatest_fit, greatest_fit_score = GeneticAlgorithm.get_greatest_fit(population)
            if greatest_fit_score > best_score:
                best_solution = greatest_fit
                best_score = greatest_fit_score
                best_solution_generation = generation_no
            else:
                max_iter -= 1
            
        print(f"  Final solution: {best_solution}, score: {best_score}")
        print(f"  Found on generation {best_solution_generation}")
        
        return best_solution
    
    def genetic_algorithm_roulette_wheel(problem, max_iter=1000000, population_size=100, mutation_rate=0.01, crossover_func=crossover, mutation_func=mutation):
        population = [[random.choice([True, False]) for _ in range(len(problem.clients))] for _ in range(population_size)]

        best_solution = population[0]
        best_score = Score.evaluate(problem, best_solution)
        best_solution_generation = 0

        generation_no = 0

        print(f"Initial solution: {best_solution}, score: {best_score}")

        while(max_iter > 0):
                
                fitness = [Score.evaluate(problem, individual) for individual in population]
                
                generation_no += 1
    
                roulette_winner_1 = GeneticAlgorithm.roulette_wheel_selection(population, fitness)
                roulette_winner_2 = GeneticAlgorithm.roulette_wheel_selection(population, fitness)

                # Crossover

                child_1, child_2 = crossover_func(roulette_winner_1, roulette_winner_2)

                # Mutation

                child_1 = mutation_func(child_1, mutation_rate)
                child_2 = mutation_func(child_2, mutation_rate)
    
                # Substituting the worst solution in the population
                population = GeneticAlgorithm.substitute_worst(problem, population, child_1)
                population = GeneticAlgorithm.substitute_worst(problem, population, child_2)
    
                # Checking the greatest fit among the current population
                greatest_fit, greatest_fit_score = GeneticAlgorithm.get_greatest_fit(population)
                if greatest_fit_score > best_score:
                    best_solution = greatest_fit
                    best_score = greatest_fit_score
                    best_solution_generation = generation_no
                else:
                    max_iter -= 1

        print(f"  Final solution: {best_solution}, score: {best_score}")
        print(f"  Found on generation {best_solution_generation}")
        
        return best_solution
    