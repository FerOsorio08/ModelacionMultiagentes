"""
Fernanda Osorio - A01026502
16 de noviembre 2023
This file contains the model class for the Roomba simulation.
"""
from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Model, DataCollector
from agent import Roomba, ObstacleAgent, TrashAgent, Charging

class RandomModel(Model):
    """ 
    It contains the funcitons: init,step and deleted_count.
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height):
        self.num_agents = N
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width,height,torus = False) 

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        
        # self.running = True 
        
        self.trash_count = 0
        # self.datacollector = DataCollector( 
        # agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, Roomba) else 0})
        self.datacollector = DataCollector( 
            agent_reporters={"Battery": lambda a: a.battery if isinstance(a, Roomba) else 0,
                        "CleanedCells": lambda a: a.cleaned_cells_count if isinstance(a, Roomba) else 0,
                        "StepsTaken": lambda a: a.steps_taken if isinstance(a, Roomba) else 0}
        
        )

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        # Add obstacles to the grid
        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)
        
        

        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):

            a = Roomba(i+1000, self, initialPos = (1,1)) 
            b = Charging(i+3000, self)
            self.schedule.add(a)
            self.schedule.add(b)
            
            #if there is only one agent place it on the 1,1 position
            if (i==0):
                pos = (1,1)

                # If the cell is not empty, keep looking for an empty cell
                while (not self.grid.is_cell_empty(pos)):
                    pos = (1,1)

                self.grid.place_agent(a, pos)
                self.grid.place_agent(b, pos)
            else:
                pos = pos_gen(self.grid.width, self.grid.height)
                while (not self.grid.is_cell_empty(pos)):
                    pos = pos_gen(self.grid.width, self.grid.height)
                self.grid.place_agent(a, pos)
                self.grid.place_agent(b, pos)
                

        # Add trash to the grid
        for i in range(20):
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(TrashAgent(i+2000, self), pos)
            self.trash_count += 1
            print("Trash count: ", self.trash_count)
        #Place trash agent in random cell

        for i in range(10):
            pos = pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            self.grid.place_agent(ObstacleAgent(i+2000, self), pos)
        
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)
        
        if self.trash_count == 0:
            print("All trash cleaned up!")
            self.running = False

    def deleted_count(self):
        """It keeps a count of the deleted trash"""
        return self.trash_count