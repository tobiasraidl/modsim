from mesa import Model
from agent import OpinionAgent, GridOpinionAgent, NetworkOpinionAgent
from utils import plot_network
from mesa.time import RandomActivation
from mesa.space import SingleGrid, NetworkGrid
import random
import seaborn as sns
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector
import statistics
import pandas as pd
import yaml
import networkx as nx

with open("params.yaml", "r") as file:
    data = yaml.safe_load(file)
    
SPACE_TYPE = data["SPACE_TYPE"]
MOORE_NEIGHBORHOOD = data["MOORE_NEIGHBORHOOD"]
PLOT_AFTER = data["PLOT_AFTER"]

class OpinionModel(Model):
    
    def __init__(self, number_agents):
        self.num_agents = number_agents
        print(number_agents)
        self.schedule = RandomActivation(self)
        self.running = True
        self.opinions_history = [{f"agent_{i}": a.opinion for i,a in enumerate(self.schedule.agents)}]
        
        self.datacollector_currents = DataCollector(
            {
                "opinion_median": OpinionModel.get_opinion_median
            }
        )
        
    def agents_meet(self, a1, a2):
        a1_opinion = a1.opinion
        a1.meet(a2.opinion)
        a2.meet(a1_opinion)
        self.opinions_history.append({f"agent_{i}": a.opinion for i,a in enumerate(self.schedule.agents)})
    
    def step(self):
        self.schedule.step()
        self.datacollector_currents.collect(self)
        if self.schedule.steps % PLOT_AFTER == 0:
            self.plot_opinion_history()
        
    def plot_opinion_history(self) -> None:
        df = pd.DataFrame(self.opinions_history)
        print(df)
        for column in df.columns:
            if column != "index":
                sns.lineplot(x=df.index, y=column, data=df)
        
        plt.xlabel("Step")
        plt.ylabel("Opinion")
        plt.title("Agent's Opinions over Time")
        plt.show()
        
    @staticmethod
    def get_opinion_median(model) -> list:
        opinions = [a.opinion for a in model.schedule.agents]
        return statistics.median(opinions)
    
class RandomOpinionModel(OpinionModel):
    def __init__(self, number_agents):
        super().__init__(number_agents)
        for i in range(self.num_agents):
                agent = GridOpinionAgent(i, self)
                self.schedule.add(agent)
        
    def step(self) -> None:
        super().step()
        id1, id2 = random.sample(range(0, self.num_agents), 2)
        a1 = self.schedule.agents[id1]
        a2 = self.schedule.agents[id2]
        self.agents_meet(a1, a2)
    
class GridOpinionModel(OpinionModel):
    def __init__(self, number_agents, width, height):
        super().__init__(number_agents)
        if SPACE_TYPE == "grid":
            self.grid = SingleGrid(width, height, True)
            self.cells = list(self.grid.coord_iter())
            # Create Agents
            for i in range(self.num_agents):
                agent = GridOpinionAgent(i, self)
                self.schedule.add(agent)

                # Add agent to a random unoccupied grid cell
                found = False
                while found == False:
                    _, pos = self.random.choice(self.cells)
                    # Check if cell is occupied
                    if self.grid.is_cell_empty(pos):
                        self.grid.place_agent(agent, pos)
                        found = True
    
    def step(self):
        super().step()
        shuffled_agents = random.sample(self.schedule.agents, len(self.schedule.agents))
        for agent in shuffled_agents:
            neighbors = self.grid.get_neighbors(agent.pos, moore=MOORE_NEIGHBORHOOD, include_center=False)
            if neighbors:
                chosen_neighbor = self.random.choice(neighbors)
                self.agents_meet(agent, chosen_neighbor)
                break
            
class NetworkOpinionModel(OpinionModel):
    def __init__(self, number_agents):
        super().__init__(number_agents)
        g = nx.Graph()
        for i in range(self.num_agents):
            agent = NetworkOpinionAgent(i, self)
            self.schedule.add(agent)
            
        agent_ids = list(range(number_agents))
        g.add_nodes_from(agent_ids)
        g.add_edges_from([(1,2), (1,3), (3,4), (1,4), (2,5), (1,6), (1,5)])
        nx.draw(g)
        self.network = NetworkGrid(g)
        
    def step(self):
        super().step()
        fig,ax=plt.subplots(1, 1, figsize=(16,10))
        f=plot_network(self, fig, layout='kamada-kawai')