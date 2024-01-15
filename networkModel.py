import matplotlib.cm
import networkx as nx
from mesa import Model

import agent
from agent import OpinionAgent
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
import random
import seaborn as sns
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector
import statistics
import pandas as pd
import yaml

with open("params.yaml", "r") as file:
    data = yaml.safe_load(file)
    
SPACE_TYPE = data["SPACE_TYPE"]
MOORE_NEIGHBORHOOD = data["MOORE_NEIGHBORHOOD"]
PLOT_AFTER = data["PLOT_AFTER"]
AVG_NODE_DEGREE = data["AVERAGE_NODE_DEGREE"]
REWIRING_PROBABILITY = data["REWIRING_PROBABILITY"]

#blue to read for political opinion, solllte einheitlich gemacht werden
cmap = matplotlib.cm.get_cmap('seismic')

class NetworkModel(Model):
    
    def __init__(self, number_agents, width, height):
        self.num_agents = number_agents
        self.schedule = RandomActivation(self)
        self.running = True
        prob = AVG_NODE_DEGREE / self.num_agents
        self.G = nx.connected_watts_strogatz_graph(n = self.num_agents, p = REWIRING_PROBABILITY, k = AVG_NODE_DEGREE)
        self.grid = NetworkGrid(self.G)

        # Create Agents
        for i, node in enumerate(self.G.nodes()):
            agent = OpinionAgent(i + 1, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, node)

            
        self.opinions_history = [{f"agent_{i}": a.opinion for i,a in enumerate(self.schedule.agents)}]
        
        self.datacollector_currents = DataCollector(
            {
                "opinion_median": NetworkModel.get_opinion_median
            }
        )


        fig, ax = plt.subplots(1, 1, figsize=(16, 10))

        self.step()
        f = self.plot_network(fig = fig, layout='kamada-kawai')
        plt.show()
        
    def agents_meet(self, a1, a2):
        a1_opinion = a1.opinion
        a1.meet(a2.opinion)
        a2.meet(a1_opinion)
        self.opinions_history.append({f"agent_{i}": a.opinion for i,a in enumerate(self.schedule.agents)})

    
    def step_network(self):
        shuffled_agents = random.sample(self.schedule.agents, len (self.schedule.agents))
        for agent in shuffled_agents:
            neighbors = self.grid.get_neighbors(agent.pos, include_center = False)
            if neighbors:
                chosen_neighbor = self.random.choice(neighbors)
                self.agents_meet(agent, chosen_neighbor)
                break
            
    def step(self):
        self.schedule.step()
        self.datacollector_currents.collect(self)

        if SPACE_TYPE == "network":
            self.step_network()
        
        if self.schedule.steps % PLOT_AFTER == 0:
            df = pd.DataFrame(self.opinions_history)
            print(df)
            for column in df.columns:
                if column != "index":
                    sns.lineplot(x=df.index, y=column, data=df)
            
            plt.xlabel("Step")
            plt.ylabel("Opinion")
            plt.title("Agent's Opinions over Time")
            plt.show()

            fig, ax = plt.subplots(1, 1, figsize=(16, 10))
            f = self.plot_network(fig=fig, layout='kamada-kawai')
            plt.show()

    def plot_network(self, fig, layout='spring', title=''):
        graph = self.G
        if layout == 'kamada-kawai':
            pos = nx.kamada_kawai_layout(graph)
        elif layout == 'circular':
            pos = nx.circular_layout(graph)
        else:
            pos = nx.spring_layout(graph, iterations=5, seed=8)

        plt.clf()
        ax = fig.add_subplot()

        opinions = [float(i.opinion) for i in self.grid.get_all_cell_contents()]

        colors = [cmap(i) for i in opinions]

        nx.draw(graph, pos, node_size=self.num_agents, edge_color = 'gray', node_color = colors, alpha = 0.9, font_size = 14, ax = ax)

        ax.set_title(title)
        return

    @staticmethod
    def get_opinion_median(model) -> list:
        opinions = [a.opinion for a in model.schedule.agents]
        return statistics.median(opinions)