""" 
Fernanda Osorio - A01026502
16 de noviembre 2023
This file contains the agent class for the Roomba model.
It has the agents: Roomba, ObstacleAgent, TrashAgent, Charging.
"""
from mesa import Agent
import networkx as nx
import matplotlib.pyplot as plt

class Roomba(Agent):
    """
    Agent that moves around the grid and cleans trash. 
    It has the funcitons: init, lowerBattery, move, detectTrash, a_star_search, heuristic, CreateGraph, GoThroughPath, 
    detectCharging, battery_threshold, step, find_nearest_charging_station. All of which are used 
    to move the agent around the grid and clean trash.
    """
    def __init__(self, unique_id, model, initialPos):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            initialPos: The initial position of the agent
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
        self.battery_thresholds = 0
        self.cleaned_cells = set()
        self.cleaned_cells_count = 0 

    #Complejidad O(N), donde N es el numero de agentes
    def clean_trash(self):
        uncleaned_cells = self.model.grid.get_cell_list_contents([self.pos])
        for trash in uncleaned_cells:
            if isinstance(trash, TrashAgent):
                self.model.grid.remove_agent(trash)
                self.model.schedule.remove(trash)
                self.cleaned_cells.add(self.pos)
                self.cleaned_cells_count = len(self.cleaned_cells)

    #Complejidad O(1)
    def lowerBattery(self):
        """
        Lowers the battery of the agent by 1
        """
        self.battery -= 1

    #Complejidad O(N), donde N es el numero de agentes
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

    #Complejidad O(N), donde N es el numero de agentes
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
            self.cleaned_cells.add(self.pos)
            self.cleaned_cells_count = len(self.cleaned_cells)
            

    #Complejidad O(E +VlogV), donde E es el numero de aristas y V el numero de vertices
    def a_star_search(self, graph, start, goal):
        """A* search to find the shortest path between a start and a goal node.
        Args:
            graph: The graph to search
            start: The start node
            goal: The goal node
        """
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
    
    #Complejidad O(1)
    def heuristic(self, a, b):
        """Manhattan distance heuristic for A* pathfinding."""
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)
    
    
    #Complejidad O(V + E), donde V es el numero de vertices y E el numero de aristas
    def CreateGraph(self):
        """Creates a graph of the visited cells"""
        self.graph = nx.grid_graph(dim=[self.model.grid.width, self.model.grid.height])

        # Get positions of obstacle agents
        obstacles_positions = [(agent.pos[0], agent.pos[1]) for agent in self.model.schedule.agents if isinstance(agent, ObstacleAgent)]

        # Remove nodes with obstacles
        self.graph.remove_nodes_from(obstacles_positions)

        return self.graph
    
    #Complejidad O(P), donde P es el numero de nodos en el path
    def GoThroughPath(self, path):
        """Moves the agent through the path"""
        #print("Moving through path")
        if path:
            current_node = path[0]
            next_node = path[1]

            # Move the agent
            self.model.grid.move_agent(self, next_node)
            self.pos = next_node

            # Remove the first node from the path
            path.pop(0)

            #print(f"Moving from {current_node} to {next_node}")
        else:
            print("No more nodes in the path.")


    #Complejidad O(1)
    def detectCharging(self):
        """Detects if the agent is in the same cell as a charging station"""
        if self.battery >= 100:
            self.charging = False
            return
        self.charging = True
        station = self.model.grid.get_cell_list_contents([self.pos])
        for agent in station:
            if isinstance(agent, Charging):
                #print("Charging +5")
                return 5
                # self.visited = []
    
    #Complejidad O(P), donde P es el numero de nodos en el path
    def battery_threshold(self):
        """Determines the battery threshold for the agent to move back home"""
        charging_station = self.find_nearest_charging_station()
        charging_path = self.a_star_search(self.CreateGraph(), self.pos, charging_station)

        if charging_path is not None:
            charging_path_length = len(charging_path)
            threshold = charging_path_length + 5  # Add a little extra for safety
            return threshold
        else:
            # If no charging path is found, return 0 (no additional battery needed)
            return 0
        

    #Complejidad O(P), donde P es el numero de nodos en el path o el numero de nodos en el grafo
    def step(self):
        """
        A single step of the agent.
        Only one action is taken every step.
        Depending on the battery level, the agent will either move or move back home to charge.
        If there is trash in the cell, the agent will clean it.
        If none of the above, the agent will move, till it finds trash or needs to charge.
        If the battery is depleted, the agent will shut down. 
        IF the battery is full, the agent will stop charging.

        """
       
        if self.battery == 0:
            #print("Battery depleted. Agent shutting down.")
            self.model.num_agents -= 1
            return

        # Check if the agent needs to move back home
        charging_station = self.find_nearest_charging_station()
        charging_path = self.a_star_search(self.CreateGraph(), self.pos, charging_station)
        #print("BATTTERY IS AT: ", self.battery, "AND LENGTH TO CHARGING STATION IS: ", len(charging_path))
        self.battery_thresholds = self.battery_threshold()
        #print("BATTERY THRESHOLD IS: ", self.battery_thresholds)

        if charging_path is not None:
            #print("Charging path is not None")
            if self.battery <= self.battery_thresholds :
                #print("Charging path:", charging_path)
                # Move back home only if the path length is less than or equal to the remaining battery
                # if charging_path is not length 1
                self.GoThroughPath(charging_path)
                if self.pos == charging_station:
                    if self.battery < 100:
                        self.battery += self.detectCharging()
                        #print("battery at: ", self.battery)
                        #min to make sure battery doesn't go over 100
                        self.battery = min(self.battery, 100)
                        self.charging = True
                    elif self.battery == 100 or self.battery > 100:
                        self.charging = False
                        #print("Battery is full")
                    
            elif self.battery > len(charging_path):
                if self.charging == True:
                    #print("Charging is true and not moving")
                    self.battery += self.detectCharging()
                    #print("battery at: ", self.battery)
                    if self.battery == 100 or self.battery > 100:
                        self.charging = False
                        #print("Battery is full")
                else:
                    self.move()
                    # Move the agent
                    # if there is trash in the cell, clean it
                    cell_contents = self.model.grid.get_cell_list_contents(self.pos)
                    if any(isinstance(agent, TrashAgent) for agent in cell_contents):
                        # There is at least one TrashAgent in the cell
                        self.detectTrash()
        else:
            #print("Just moving")
            self.move()
            # Move the agent
            # if there is trash in the cell, clean it
            cell_contents = self.model.grid.get_cell_list_contents(self.pos)
            if any(isinstance(agent, TrashAgent) for agent in cell_contents):
                # There is at least one TrashAgent in the cell
                self.detectTrash()


    #Complejidad O(C) donde C es el numero de estaciones de carga
    def find_nearest_charging_station(self):
        """Finds the nearest charging station using simple distance calculation."""
        charging_stations = [agent.pos for agent in self.model.schedule.agents if isinstance(agent, Charging)]
        self.graph.add_nodes_from(charging_stations)
        distances = [self.heuristic(self.pos, station) for station in charging_stations]
        if distances:
            #print("Charging stations:", charging_stations)
            #print("Choosen charging station:", charging_stations[distances.index(min(distances))])
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
        #pass to make sure it doesn't move
        pass

class Charging(Agent):
    """
    Charging agent. Just to add charging stations to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass