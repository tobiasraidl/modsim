from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import OpinionModel
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import NumberInput
import yaml

with open("params.yaml", "r") as file:
    data = yaml.safe_load(file)

NUMBER_AGENTS = data["NUMBER_AGENTS"]

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

simulation_params = {
    "number_agents": NumberInput(
        "Choose how many agents to include in the model", value=NUMBER_AGENTS
    ),
    "width": NUMBER_AGENTS,
    "height": NUMBER_AGENTS,
}

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    
    if agent.opinion > 2/3:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.5
    elif agent.opinion > 1/3:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.4
    else:
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.3
    return portrayal

grid = CanvasGrid(
    agent_portrayal,
    NUMBER_AGENTS,
    NUMBER_AGENTS,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)

chart_currents = ChartModule(
    [
        {"Label": "opinion_median", "Color": "black"},
    ],
    canvas_height=300,
    data_collector_name="datacollector_currents"
)

server = ModularServer(OpinionModel, 
                       [grid, chart_currents], 
                       "Opinion Model", 
                       simulation_params)
server.port = 8521
server.launch()

