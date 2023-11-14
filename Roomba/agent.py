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
        obstacle_neighbors = [n for n in possible_steps if any(isinstance(agent, ObstacleAgent) for agent in self.model.grid.get_cell_list_contents(n))]
        trash_neighbors = [n for n in possible_steps if any(isinstance(agent, TrashAgent) for agent in self.model.grid.get_cell_list_contents(n))]
        charging_neighbors = [n for n in possible_steps if any(isinstance(agent, Charging) for agent in self.model.grid.get_cell_list_contents(n))]

        if obstacle_neighbors:
            free_spaces_away = [p for p in possible_steps if p not in obstacle_neighbors and self.model.grid.is_cell_empty(p)]
            next_move = self.random.choice(free_spaces_away) if free_spaces_away else self.random.choice(possible_steps)
            self.battery -= 1
        elif trash_neighbors:
            next_move = self.random.choice(trash_neighbors)
            self.battery -= 1
        elif self.battery < 20 and charging_neighbors:
            next_move = self.random.choice(charging_neighbors) if charging_neighbors else self.random.choice(possible_steps)
            self.battery += 100
        else:
            next_move = self.random.choice(possible_steps)
            self.battery -= 1

        if self.battery == 0:
            self.model.running = False
            print("Battery is 0, stopping simulation")

        # Now move: this for many roombas
        # if self.random.random() < 0.1:
        #     self.visited_cells.add(self.pos)
        #     self.model.grid.move_agent(self, next_move)
        #     self.steps_taken += 1
        #Move for 1 roomba
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

class Charging(Agent):
    """
    Charging agent. Just to add charging stations to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass