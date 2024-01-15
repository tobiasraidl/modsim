from mesa import Agent
import numpy as np
import random
import yaml

with open("params.yaml", "r") as file:
    data = yaml.safe_load(file)

TAU = data["TAU"]
MU = data["MU"]
SPACE_TYPE = data["SPACE_TYPE"]
MOORE_NEIGHBORHOOD = data["MOORE_NEIGHBORHOOD"]

class OpinionAgent(Agent):
    
    def __init__(self, id, model):
        super().__init__(id, model)
        self.opinion = np.random.uniform(0, 1)
        self.id = id
    
    def step(self) -> None:
        self.move()

    
    def move(self) -> None:
        if SPACE_TYPE == "grid":
            # Check for free cells in neighborhood
            available_cells = self.model.grid.get_neighborhood(
                self.pos,
                moore=MOORE_NEIGHBORHOOD,
                include_center=False)

            idxs = [i for i in range(0, len(available_cells))]
            random.shuffle(idxs)

            # Choose a random unoccupied neighboring cell
            for idx in idxs:
                cell = available_cells[idx]
                if (self.model.grid.is_cell_empty(cell)):
                    self.model.grid.move_agent(self, cell)
        
    def meet(self, partner_opinion):
        if abs(self.opinion-partner_opinion) <= TAU:
            self.opinion = self.opinion + MU * (partner_opinion - self.opinion)