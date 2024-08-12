import random
import copy

class Problem:
    def __init__(self, clients, ingredients):
        # List of dictionaries representing clients' preferences
        self.clients = clients
        # List of unique ingredients mentioned in the input file
        self.ingredients = ingredients
        self.list_bool_ing = [False for _ in range(len(ingredients))]

    # return the initial state (empty set of ingredients)
    def initial_state(self):
        return set()  
    
    # add an ingredient to the list of boolean ingredients
    def add_ingredient(self, ingredient):
        ingredient_index = self.ingredients.index(ingredient)
        self.list_bool_ing[ingredient_index] = True

    # remove an ingredient from the list of boolean ingredients
    def remove_ingredient(self, ingredient):
        ingredient_index = self.ingredients.index(ingredient)
        self.list_bool_ing[ingredient_index] = False

    # return the boolean value of an ingredient
    def get_ingredient_bool(self, ingredient):
        ingredient_index = self.ingredients.index(ingredient)
        return self.list_bool_ing[ingredient_index]
    
    # return the list of boolean ingredients
    def get_list_bool(self):
        return self.list_bool_ing
    
    # set the list of boolean ingredients
    def set_list_bool(self, list_bool):
        self.list_bool_ing = list_bool

    # return the list of ingredients that are true
    def get_list_ingredients_true(self, list_bool):
        return [self.ingredients[i] for i in range(len(list_bool)) if list_bool[i]]

    # return a list of neighboring states of the current state
    def get_neighbors(self, state):
        neighbors = []
        for _ in range(10):  # Generate 10 neighbors
            client = random.choice(self.clients)
            if random.random() < 0.5:  # Add an ingredient
                like = random.choice(client['likes'])
                if like not in state:
                    new_state = state.copy()
                    new_state.add(like)
                    neighbors.append(new_state)
            else:  # Remove an ingredient
                if client['dislikes']:  # Check if dislikes list is not empty
                    dislike = random.choice(client['dislikes'])
                    if dislike in state:
                        new_state = state.copy()
                        new_state.remove(dislike)
                        neighbors.append(new_state)
        return neighbors
    
    # return a list of neighboring states of the current state
    def get_neighbours_bool(self, list_bool):
        neighbors = []
        neighbour = copy.deepcopy(list_bool)
        for i in range(len(list_bool)):
            if random.random() < 0.5:
                neighbour[i] = not neighbour[i]
        return neighbour

    # evaluate the state based on the number of satisfied clients
    def evaluate(self, state):
        score = 0
        for client in self.clients:
            if all(like in state for like in client['likes']) and not any(dislike in state for dislike in client['dislikes']):
                score += 1
        return score