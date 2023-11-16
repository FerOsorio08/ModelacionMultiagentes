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

    def lowerBattery(self):
        """
        Lowers the battery of the agent by 1
        """
        self.battery -= 1

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        free_spaces = [possible_steps[i] for i in range(len(possible_steps)) if self.model.grid.is_cell_empty(possible_steps[i])]
        trash_neighbors = [agent.pos for agent in self.model.grid.get_cell_list_contents(possible_steps) if isinstance(agent, TrashAgent)]

        next_moves = trash_neighbors if trash_neighbors else free_spaces 
        next_moves_non_visited = list(set(next_moves) - self.visited_cells)

        if next_moves:
            next_move = self.random.choice(next_moves)
        elif next_moves_non_visited:
            next_move = self.random.choice(next_moves_non_visited)
        
        else:
            # No valid move, stay in the current position
            return

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
            self.model.trash_count -= 1
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
        self.graph.add_edges_from([(coordinates[i], coordinates[i + 1]) for i in range(len(coordinates) - 1)] + [(coordinates[-1], coordinates[0])])
        # Create edges between adjacent nodes
        # print("Coordinates:", coordinates)
        # print("Edges:", self.graph.edges)
        for i in range(len(coordinates) - 1):
            x1, y1 = coordinates[i]
            for j in range(i + 1, len(coordinates)):
                x2, y2 = coordinates[j]
                if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    self.graph.add_edge(coordinates[i], coordinates[j])
        return self.graph
    
    def backHome(self, path):
        print("In backHome")
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]

            # Move the agent
            self.model.grid.move_agent(self, next_node)
            self.pos = next_node  # Update the agent's position in the Mesa model

            # Update visited_cells
            self.visited_cells.add(next_node)

            print(f"Moving from {current_node} to {next_node}")

        # Exclude the goal node from the path
        goal_node = path[-1]
        print("Goal Node:", goal_node)
        print("Moving back to the initial position:", self.initialPos)
    
    def GoThroughPath(self, path):
        """Moves the agent through the path"""
        print("moving through path")
        for i in range(len(path) - 1):
            current_node = path[i]
            print ("current node", current_node)
            next_node = path[i + 1]
            print ("next node", next_node)

            # Move the agent
            self.model.grid.move_agent(self, next_node)
            self.pos = next_node



    def detectCharging(self):
        if self.battery >= 100:
            self.charging = False
            return

        self.charging = True
        station = self.model.grid.get_cell_list_contents([self.pos])
        for agent in station:
            if isinstance(agent, Charging):
                print("Charging to 100%")
                self.battery += 100
                # self.visited = []

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if self.battery == 0:
            print("Battery depleted. Agent shutting down.")
            self.model.num_agents -= 1
            return

        # Check if the agent needs to move back home
        charging_station = self.find_nearest_charging_station()
        charging_path = self.a_star_search(self.CreateGraph(), self.pos, charging_station)

        if charging_path is not None: 
            print("charging path is not none")
            if charging_path and len(charging_path) > 4 and len(charging_path) <= self.battery:
                print("Charging path:", charging_path)
                # Move back home only if the path length is less than or equal to the remaining battery
                # if charging_path is not length 1
                if len(charging_path) != 1:
                    self.GoThroughPath(charging_path)
                    if self.pos == charging_station:
                        self.detectCharging()

            elif self.battery > len(charging_path):
                self.move()
                # Move the agent
                # if there is trash in the cell, clean it
                cell_contents = self.model.grid.get_cell_list_contents(self.pos)
                if any(isinstance(agent, TrashAgent) for agent in cell_contents):
                    # There is at least one TrashAgent in the cell
                    self.detectTrash()
        else: 
            print("just moving")
            self.move()
            # Move the agent
            # if there is trash in the cell, clean it
            cell_contents = self.model.grid.get_cell_list_contents(self.pos)
            if any(isinstance(agent, TrashAgent) for agent in cell_contents):
                # There is at least one TrashAgent in the cell
                self.detectTrash()
            

        # Other actions as needed
        # self.ExploreCell()

    def find_nearest_charging_station(self):
        """Finds the nearest charging station using simple distance calculation."""
        charging_stations = [agent.pos for agent in self.model.schedule.agents if isinstance(agent, Charging)]
        charging_stations.append(self.initialPos)
        # charging_stations = list(set(charging_stations) - self.visited_cells)
        self.graph.add_nodes_from(charging_stations)
        distances = [self.heuristic(self.pos, station) for station in charging_stations]
        if distances:
            return charging_stations[distances.index(min(distances))]
        else:
            # No charging stations found, return the initial position as a fallback
            return self.initialPos



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