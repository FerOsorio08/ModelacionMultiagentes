from model import RandomModel, ObstacleAgent, TrashAgent, Charging
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.4
    
    if (isinstance(agent, TrashAgent)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3
    
    if (isinstance(agent, Charging)):
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

model_params = {"N":1, "width":12, "height":12}

grid = CanvasGrid(agent_portrayal, 12, 12, 500, 500)

# bar_chart = BarChartModule(
#     [{"Label":"Steps", "Color":"#AA0000"}], 
#     scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RandomModel, [grid], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()