from mesa import Agent

class Roomba(Agent):
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
        self.visited_cells = set()

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False # Boolean for whether to include the center cell itself as one of the neighbors
            ) 
        
        # Checks which grid cells are empty
        # Get the neighbors that have trash
        obstacle_neighbors = [neighbor for neighbor in possible_steps if any(isinstance(agent, ObstacleAgent) for agent in self.model.grid.get_cell_list_contents(neighbor))]

        # If there are neighbors with obstacles, prioritize moving away from them
        if obstacle_neighbors:
            free_spaces_away_from_obstacles = [p for p in possible_steps if p not in obstacle_neighbors and self.model.grid.is_cell_empty(p)]
            if free_spaces_away_from_obstacles:
                next_move = self.random.choice(free_spaces_away_from_obstacles)
            else:
                # If there are no free spaces away from obstacles, move randomly
                next_move = self.random.choice(possible_steps)
        
        else:
            trash_neighbors = [neighbor for neighbor in possible_steps if any(isinstance(agent, TrashAgent) for agent in self.model.grid.get_cell_list_contents(neighbor))]

            # If there are neighbors with trash, prioritize moving to one of them
            if trash_neighbors:
                # next_move = self.choice(trash_neighbors)
                next_move = self.random.choice(trash_neighbors)
            else:
                # If there are no neighbors with trash, prioritize moving to an unvisited cell
                unvisited_cells = [p for p in possible_steps if p not in self.visited_cells]
                if unvisited_cells:
                    next_move = self.random.choice(unvisited_cells)
                else:
                    # If all cells have been visited, choose a random empty cell
                    freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))
                    next_moves = [p for p, f in zip(possible_steps, freeSpaces) if f]
                    next_move = self.random.choice(next_moves)

        # Now move: this for many roombas
        # if self.random.random() < 0.1:
        #     self.visited_cells.add(self.pos)
        #     self.model.grid.move_agent(self, next_move)
        #     self.steps_taken += 1
        #Move for 1 roomba
        self.visited_cells.add(self.pos)
        self.model.grid.move_agent(self, next_move)
        self.steps_taken += 1
 

        # If the agent can't move, then it stays put
        #map : apply a function to every item of an iterable, and return a list of the results
        #zip : make an iterator that aggregates elements from each of the iterables
        
    
    
    def detectTrash(self):
        """
        Detects if there is trash in the same cell as the agent
        """
        cell_contents = self.model.grid.get_cell_list_contents(self.pos)
        trash_agents = [agent for agent in cell_contents if isinstance(agent, TrashAgent)]

        if trash_agents:
            # If there is trash in the cell, "delete" the TrashAgent
            trash_agent = trash_agents[0]  # Assuming there is at most one trash agent in the cell
            self.model.grid.remove_agent(trash_agent)
    
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()
        self.detectTrash()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class TrashAgent(Agent):
    """
    Trash agent. Just to add trash to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass