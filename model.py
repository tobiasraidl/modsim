from mesa import Model
from agent import OpinionAgent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
import seaborn as sns
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector
import statistics
import pandas as pd

class OpinionModel(Model):
    
    def __init__(self, number_agents, width, height):
        self.num_agents = number_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        
        # Create Agents
        for i in range(self.num_agents):
            agent = OpinionAgent(i, self)
            self.schedule.add(agent)
            
            # Add agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x,y))
            
        self.opinions_history = [{f"agent_{i}": a.opinion for i,a in enumerate(self.schedule.agents)}]
        
        self.datacollector_currents = DataCollector(
            {
                "opinion_median": OpinionModel.get_opinion_median
            }
        )
            
    def step(self):
        self.schedule.step()
        self.datacollector_currents.collect(self)
        id1, id2 = random.sample(range(0, self.num_agents), 2)
        a1 = self.schedule.agents[id1]
        a2 = self.schedule.agents[id2]
        a1_opinion = a1.opinion
        a1.meet(a2.opinion)
        a2.meet(a1_opinion)
        
        self.opinions_history.append({f"agent_{i}": a.opinion for i,a in enumerate(self.schedule.agents)})
        if self.schedule.steps % 1000 == 0:
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