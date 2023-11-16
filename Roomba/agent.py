from mesa import Agent
import networkx as nx
import matplotlib.pyplot as plt

class Roomba(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, initialPos):
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
        self.graph = nx.Graph()
        self.graph.add_node(initialPos)
        self.initialPos = initialPos

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

        if trash_agents:
            # Assuming there is at most one trash agent in the cell
            trash_agent = trash_agents[0]
            # "Clean up" the trash agent
            self.model.grid.remove_agent(trash_agent)
            self.lowerBattery()

    def a_star_search(self, graph, start, goal):
        """A* search to find the shortest path between a start and a goal node.
        Args:
            graph: The graph to search
            start: The start node
            goal: The goal node
        """
        # self.graph.add_node((1,1))
        # self.graph.add_node(self.pos)
        self.graph.add_node(self.initialPos)
        x, y = start
        j, i = goal
        heuristic  = abs(x - j) + abs(y - i)
        try:
            path = nx.astar_path(graph, start, goal, heuristic=self.heuristic)
            return path
        except nx.NetworkXNoPath:
            # If no path is found, return None
            return None
    
    def heuristic(self, a, b):
        """Manhattan distance heuristic for A* pathfinding."""
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)
    
    
    def CreateGraph(self):
        """Creates a graph of the visited cells"""
        self.visited_cells.add((self.initialPos))
        self.visited_cells.add(self.pos)
        coordinates = list(self.visited_cells)
        self.graph.add_nodes_from(coordinates)
        # Create edges between adjacent nodes
        print("Coordinates:", coordinates)
        print("Edges:", self.graph.edges)
        for i in range(len(coordinates) - 1):
            x1, y1 = coordinates[i]
            for j in range(i + 1, len(coordinates)):
                x2, y2 = coordinates[j]
                if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    self.graph.add_edge(coordinates[i], coordinates[j])
        return self.graph
    
    def backHome(self):
        print("In back home")
        # self.visited_cells.add((1, 1))
        # self.visited_cells.add(self.pos)

        # coordinates = list(self.visited_cells)  # Convert set to list
        # self.graph.add_nodes_from(coordinates)

        # # Create edges between adjacent nodes
        # for i in range(len(coordinates) - 1):
        #     x1, y1 = coordinates[i]
        #     for j in range(i + 1, len(coordinates)):
        #         x2, y2 = coordinates[j]
        #         if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
        #             self.graph.add_edge(coordinates[i], coordinates[j])
        self.CreateGraph()

        start_node = self.pos
        goal_node = self.initialPos
        print("Start Node:", start_node)

        # Print the coordinates and edges for debugging
        

        path = self.a_star_search(self.graph, start_node, goal_node,)
        print("Path:", path)

        if path and len(path) > 1:
            next_position = path[1]
            print("Next Position:", next_position)

            # Move the agent
            self.model.grid.move_agent(self, next_position)
            self.pos = next_position  # Update the agent's position in the Mesa model

            # Update visited_cells
            self.visited_cells.add(next_position)
            return path
        else:
            print("No valid path found.")
            return None

    
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


    def detectCharging(self):
        if self.battery >= 100:
            self.charging = False
            return

        self.charging = True
        station = self.model.grid.get_cell_list_contents([self.pos])
        for agent in station:
            if isinstance(agent, Charging):
                self.battery += 5
                self.visited = []

    
    # def step(self):
    #     """ 
    #     Determines the new direction it will take, and then moves
    #     """
    #     self.move()
    #     self.detectTrash()
    #     # path_to_home = self.backHome()
    #     if self.battery <= 53:
    #         self.backHome()
    #     #     self.detectCharging()
    #     # if len(path_to_home) <= self.battery:
    #     #     self.backHome()
    #     #     self.detectCharging()
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()
        self.detectTrash()
        print("Initial Position:", self.initialPos)  # Fix here
        
        # Calculate the path back to the charging station
        charging_path = self.a_star_search(self.CreateGraph(), self.pos, self.initialPos)  # Fix here

        if charging_path and len(charging_path) == self.battery:
            print("Charging path:", charging_path)
            # Move back home only if the path length is equal to the battery level
            self.backHome()
        else:
            self.detectCharging()

        # Other actions as needed
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