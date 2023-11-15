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

        self.direction = 4
        self.steps_taken = 0
        self.visited_cells = set()
        self.battery = 100
        self.charging = False
        # obstacle_neighbors = []
        # trash_neighbors = []
        # charging_neighbors = []
        # unvisited_neighbors = []

    def lowerBattery(self):
        """
        Lowers the battery of the agent by 1
        """
        self.battery -= 1

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        if self.battery == 0:
            print("battery 0")
            self.model.num_agents -= 1
            return
        
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False # Boolean for whether to include the center cell itself as one of the neighbors
            )
        
        trash_neighbors = self.model.grid.get_cell_list_contents(possible_steps)
        trash_pos = []
        for agent in trash_neighbors:
            if isinstance(agent, TrashAgent):
                trash_pos.append(agent.pos)
        
        # unvisited_neighbors = [neighbor for neighbor in possible_steps if neighbor not in self.visited_cells]
        # next_move = self.random.choice(unvisited_neighbors)
        free_spaces = list(map(self.model.grid.is_cell_empty, possible_steps))
        next_moves = []
        if trash_pos:
            next_moves = trash_pos
        else :
            for i in range(len(free_spaces)):
                if free_spaces[i]:
                    next_moves.append(possible_steps[i])
        next_moves_nonVisited = list(set(next_moves) - set(self.visited_cells))
        next_move = self.random.choice(next_moves_nonVisited) if len(next_moves_nonVisited) > 0 else self.random.choice(next_moves)

        

        # Now move: this for many roombas
        # if self.random.random() < 0.1:
        #     self.visited_cells.add(self.pos)
        #     self.model.grid.move_agent(self, next_move)
        #     self.steps_taken += 1
        #Move for 1 roomba
        self.visited_cells.add(self.pos)
        self.model.grid.move_agent(self, next_move)
        self.steps_taken += 1
        self.lowerBattery()
 
    
    
    def detectTrash(self):
        """
        Detects if there is trash in the same cell as the agent
        """
        cell_contents = self.model.grid.get_cell_list_contents(self.pos)
    
        # Check if there is a TrashAgent in the cell
        trash_agents = [agent for agent in cell_contents if isinstance(agent, TrashAgent)]
        print("trash", trash_agents)

        if trash_agents:
            # Assuming there is at most one trash agent in the cell
            trash_agent = trash_agents[0]
            # "Clean up" the trash agent
            self.model.grid.remove_agent(trash_agent)
            self.lowerBattery()

    
    def detectObstacle(self):
        """Detect the Obstacle Agents in neighboring cells and avoid them"""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False) 
    
    def ExploreCell(self):
        """
        Detects if there is an obstacle in the same cell as the agent
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=False) 
        # Boolean for whether to include the center cell itself as one of the neighbors

        free_cell = [neighbor for neighbor in possible_steps if neighbor not in self.visited_cells]
        next_move = self.random.choice(free_cell)
        # cell_contents = other.model.grid.get_cell_list_contents(other.pos)
        # obstacle_agents = [agent for agent in cell_contents if isinstance(agent, ObstacleAgent)]
        self.model.grid.move_agent(self, next_move)
        self.visited_cells.add(self.pos)
        self.steps_taken += 1
        self.lowerBattery()

    
    def return_to_station(self):
        if self.battery == 0:
            self.model.num_agents -= 1
            return

        if len(self.visited_cells) == 0:
            self.recharge()
            return

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            moore=True,
            include_center=False)

        possibleStation = self.model.grid.get_cell_list_contents(
            possible_steps)

        isStation = False
        isAgent = False

        for agent in possibleStation:
            # check if there is a load station in the possible steps and if that station doesnt have an agent on it
            if isinstance(agent, LoadStation):
                isStation = True
            if isinstance(agent, RandomAgent):
                isAgent = True

        if isStation and not isAgent:
            self.model.grid.move_agent(self, agent.pos)
            self.steps_taken += 1
            self.battery -= 1
            self.detectCharging()
            return

        # find the first time your currrent position is in the array
        for i in range(len(self.visited)):
            if self.visited[i] == self.pos:
                if i == 0:
                    self.recharge()
                    return
                self.model.grid.move_agent(self, self.visited[i-1])
                self.steps_taken += 1
                self.battery -= 1
                return

        self.model.grid.move_agent(self, self.visited[-1])

    def detectCharging(sFalse):
        if self.battery >= 100:
            self.charging = False
            return

        self.charging = True
        station = self.model.grid.get_cell_list_contents([self.pos])
        for agent in station:
            if isinstance(agent, Charging):
                self.battery += 5
                self.visited = []

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()
        self.detectTrash()
        self.detectObstacle()
        # self.ExploreCell()
        # self.detectCharging()
        
        # self.ExploreCell()

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