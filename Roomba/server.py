from model import RandomModel, ObstacleAgent, TrashAgent, Charging
from mesa.visualization import CanvasGrid, BarChartModule, PieChartModule
from mesa.visualization import ModularServer
from mesa.datacollection import DataCollector

COLORS = {"Cleaned": "purple", "StepsTaken": "black", "Battery": "green"}


def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}

    if isinstance(agent, ObstacleAgent):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.6
    
    if isinstance(agent, TrashAgent):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3
    
    if isinstance(agent, Charging):
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

model_params = {"N": 3, "width": 12, "height": 12, "trash_countS": 20}

grid = CanvasGrid(agent_portrayal, 12, 12, 500, 500)

bar_chart = BarChartModule(
    [
        {"Label": "Battery", "Color": "purple"},
        {"Label": "CleanedCells", "Color": "green"},
        {"Label": "StepsTaken", "Color": "black"}
    ],
    scope="agent",
    sorting="ascending",
    sort_by="Steps",
    canvas_height=300,  
    canvas_width=300,
)

# pie_chart = PieChartModule(
#     [{"Label": label, "Color": color} for label, color in COLORS.items()]
# )


server = ModularServer(RandomModel, [grid, bar_chart], "Roomba Agents", model_params)
server.port = 8521  # The default
server.launch()
