# score.py
# Evaluate the score of a solution based on the number of clients satisfied
class Score:
    @staticmethod
    def evaluate(problem, solution):
        score = 0
        for client in problem.clients:
            if all(like in solution for like in client['likes']) and not any(dislike in solution for dislike in client['dislikes']):
                score += 1
        return score

    def evaluate_bool(problem, list_bool):
        score = 0
        ingredient_indices = {ingredient: i for i, ingredient in enumerate(problem.ingredients)}
        for client in problem.clients:
            if all(list_bool[ingredient_indices[like]] for like in client['likes']) and not any(list_bool[ingredient_indices[dislike]] for dislike in client['dislikes']):
                score += 1
        return score