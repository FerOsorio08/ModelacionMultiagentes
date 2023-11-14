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
        self.battery = 100
        obstacle_neighbors = []
        trash_neighbors = []
        charging_neighbors = []
        unvisited_neighbors = []

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False # Boolean for whether to include the center cell itself as one of the neighbors
            )
        
        unvisited_neighbors = [neighbor for neighbor in possible_steps if neighbor not in self.visited_cells]
        next_move = self.random.choice(unvisited_neighbors)
        

        # Now move: this for many roombas
        # if self.random.random() < 0.1:
        #     self.visited_cells.add(self.pos)
        #     self.model.grid.move_agent(self, next_move)
        #     self.steps_taken += 1
        #Move for 1 roomba
        x = self.pos[0]
        y = self.pos[1]
        self.visited_cells.add(self.pos)
        self.model.grid.move_agent(self, next_move)
        self.steps_taken += 1
        self.battery -= 1
 
    
    
    def detectTrash(self):
        """
        Detects if there is trash in the same cell as the agent
        """
        cell_contents = self.model.grid.get_cell_list_contents(self.pos)
        trash_agents = [agent for agent in cell_contents if isinstance(agent, TrashAgent)]

        if trash_agents:
            # If there is trash in the cell, "delete" the TrashAgent
            trash_agent = trash_agents[0]  # Assuming there is at most one trash agent in the cell
            self.model.grid.remove_agent(next_move)
    
    def ShortestPathtoTrash(self):
        """
        Finds the shortest path to the nearest trash
        """
        pass

    def detectCharging(self):
        """
        Detects if there is a charging station in the same cell as the agent
        """
        cell_contents = self.model.grid.get_cell_list_contents(self.pos)
        charging_agents = [agent for agent in cell_contents if isinstance(agent, Charging)]

        if charging_agents:
            # If there is a charging station in the cell, "delete" the Charging agent
            charging_agent = charging_agents[0]
    
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()
        self.detectTrash()
        self.detectCharging()

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

class Charging(Agent):
    """
    Charging agent. Just to add charging stations to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass