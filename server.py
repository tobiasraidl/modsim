from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import OpinionModel
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import NumberInput
import yaml

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    
    if agent.opinion > 4/5:
        portrayal["Color"] = "#ff6666"
        portrayal["Layer"] = 0
    elif agent.opinion > 3/5:
        portrayal["Color"] = "#ffc466"
        portrayal["Layer"] = 1
    elif agent.opinion > 2/5:
        portrayal["Color"] = "#fffa66"
        portrayal["Layer"] = 2
    elif agent.opinion > 1/5:
        portrayal["Color"] = "#bdff66"
        portrayal["Layer"] = 3
    else:
        portrayal["Color"] = "#69ff66"
        portrayal["Layer"] = 4
    return portrayal

def main():
    with open("params.yaml", "r") as file:
        data = yaml.safe_load(file)

    NUMBER_AGENTS = data["NUMBER_AGENTS"]
    GRID_SIZE = data["GRID_SIZE"]

    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = 500

    simulation_params = {
        "number_agents": NumberInput(
            "Choose how many agents to include in the model", value=NUMBER_AGENTS
        ),
        "width": GRID_SIZE,
        "height": GRID_SIZE,
    }
    
    grid = CanvasGrid(
        agent_portrayal,
        GRID_SIZE,
        GRID_SIZE,
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

if __name__ == "__main__":
    main()