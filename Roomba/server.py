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
        portrayal["r"] = 0.6
    
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

bar_chart = BarChartModule(
    [
        {"Label": "Battery", "Color": "green"},
        {"Label": "CleanedCells", "Color": "red"},
        {"Label": "StepsTaken", "Color": "blue"}
    ],
    scope="agent",
    sorting="ascending",
    sort_by="Steps",
    canvas_height=300,  
    canvas_width=300,

)


# bar_chart2 = BarChartModule([{"Label": "Deleted_Count", "Color": "red"}], scope="model")

server = ModularServer(RandomModel, [grid, bar_chart], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()