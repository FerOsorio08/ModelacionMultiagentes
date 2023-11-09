from mesa import Agent

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        ## 1 = North, 2 = North-East, 3 = East, 4 = South-East, 5 = South, 6 = South-West, 7 = West, 8 = North-West

        self.direction = 4
        self.steps_taken = 0

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) # Boolean for whether to include the center cell itself as one of the neighbors
        
        # Checks which grid cells are empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        # If the agent can't move, then it stays put
        #map : apply a function to every item of an iterable, and return a list of the results
        #zip : make an iterator that aggregates elements from each of the iterables
        next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
       
        next_move = self.random.choice(next_moves)

        # Now move:
        if self.random.random() < 0.1:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken+=1

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  
