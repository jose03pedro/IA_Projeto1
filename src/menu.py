# menu.py
class Menu:
    @staticmethod
    def choose_algorithm():
        print("Choose an algorithm: ")
        print("1: Hill Climbing")
        print("2: Tabu Search")
        print("3: Genetic Algorithm Tournament")
        print("4: Genetic Algorithm Roulette Wheel")
        print("5: Genetic Algorithm Fitness")
        print("6: Simulated Annealing")
        print("Choice: ", end="")
        choice = int(input())
        switch = {
            1: 'hill_climbing',
            2: 'tabu_search',
            3: 'genetic_algorithm_tournament',
            4: 'genetic_algorithm_roulette_wheel',
            5: 'genetic_algorithm_fitness',
            6: 'simulated_annealing'
        }
        
        if choice in switch:
            return switch[choice]
        else:
            print("Invalid choice")
            return None

    @staticmethod
    def choose_file():
        print("Choose a file to read: ")
        print("1: An example")
        print("2: Basic")
        print("3: Coarse")
        print("4: Difficult")
        print("5: Elaborate")
        print("Choice: ", end="")
        choice = int(input())
        switch = {
            1: '../input/a_an_example.in.txt', 
            2: '../input/b_basic.in.txt',
            3: '../input/c_coarse.in.txt',
            4: '../input/d_difficult.in.txt',
            5: '../input/e_elaborate.in.txt'
        }
        
        if choice in switch:
            return switch[choice]
        else:
            print("Invalid choice")
            return None