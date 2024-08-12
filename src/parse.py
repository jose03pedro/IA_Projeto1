# parse.py
class Parse:
    @staticmethod
    def read_input_file(file_path):
        # Open the input file in read mode
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Extract the number of clients from the first line of the file
        num_clients = int(lines[0].strip())
        clients = []  # Initialize an empty list to store client data
        ingredients = set()  # Initialize an empty set to store unique ingredients

        # Iterate through client data in the file
        for i in range(1, 2*num_clients+1, 2):
            likes_line = lines[i].strip().split()  # Split the line containing client likes
            dislikes_line = lines[i+1].strip().split()  # Split the line containing client dislikes

            # Extract likes information
            num_likes = int(likes_line[0])
            likes = likes_line[1:num_likes+1]
            ingredients.update(likes)  # Add likes to the set of unique ingredients

            # Extract dislikes information
            num_dislikes = int(dislikes_line[0])
            dislikes = dislikes_line[1:num_dislikes+1]
            ingredients.update(dislikes)  # Add dislikes to the set of unique ingredients

            # Create a dictionary representing the client with likes and dislikes
            client = {'likes': likes, 'dislikes': dislikes}
            clients.append(client)  # Add the client to the list of clients

        # Return the list of clients and the list of unique ingredients
        return clients, list(ingredients)