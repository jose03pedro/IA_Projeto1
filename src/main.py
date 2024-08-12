from menu import Menu  
from parse import Parse  
from score import Score  
from algorithms import Algorithms  
from problem import Problem  
import time  

def main():
    # Prompt user to choose a file
    file_path = Menu.choose_file()
    # If no file is chosen, exit the program
    if file_path is None:
        return
    
    # Read the input file 
    clients, ingredients = Parse.read_input_file(file_path)
    # Create a Problem instance 
    problem = Problem(clients, ingredients)
    
    # Prompt user to choose an algorithm 
    algorithm_name = Menu.choose_algorithm()
    # If no algorithm is chosen, exit the program
    if algorithm_name is None:
        return
    
    # Get the algorithm function
    algorithm = getattr(Algorithms, algorithm_name)
    
    # Record the starting time
    start_time = time.time()
    # Execute the chosen algorithm on the problem
    solution = algorithm(problem)
    # Record the ending time
    end_time = time.time()
    
    # Evaluate the solution score based on the chosen algorithm
    if algorithm_name in ['genetic_algorithm_tournament', 'genetic_algorithm_roulette_wheel', 'genetic_algorithm_fitness', 'simulated_annealing']:
        print("Solution: ", problem.get_list_ingredients_true(solution))
        print("Score: ", Score.evaluate(problem, problem.get_list_ingredients_true(solution)))
    else:
        print("Solution: ", solution)
        print("Score: ", Score.evaluate(problem, solution))
    
    # Calculate and print the time taken for the algorithm to run
    final_time = end_time - start_time
    print("Time taken: ", round(final_time, 2), "seconds")

if __name__ == "__main__":
    main()
