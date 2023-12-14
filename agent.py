from mesa import Agent
import numpy as np
import random
import yaml

with open("params.yaml", "r") as file:
    data = yaml.safe_load(file)

TAU = data["TAU"]
MU = data["MU"]

class OpinionAgent(Agent):
    
    def __init__(self, id, model):
        super().__init__(id, model)
        self.opinion = np.random.uniform(0,1)
        self.id = id
    
    def step(self) -> None:
        self.move()
    
    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, 
            moore=True, 
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
    def meet(self, partner_opinion):
        if abs(self.opinion-partner_opinion) <= TAU:
            self.opinion = self.opinion + MU * (partner_opinion - self.opinion)