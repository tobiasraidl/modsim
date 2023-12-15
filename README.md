# Agent Based Opinion Model
Random, grid and network structured agent based opinion models  
Configurate model parameters in params.yaml  
Execute server.py in order to run the model  

![plot](./example_lineplot.png)

## Random Model
Each step 2 agents are randomly selected.

## Grid Model
Each step 2 neighboring agents are randomly selected.

## Network Model
Not yet started

## TODO
- [x] Implement logic for agents to not move on occupied fields
- [x] Implement logic for agent initialization to only get placed on unoccupied cells
- [x] Implement easy switch between random and grid version (boolean in param.yaml?)
- [x] Better color scheme for grid representation
- [x] Implement logic for agent meetups in grid version
- [ ] Implement network version
- [ ] Make initial opinion distribution normal
- [ ] ...

### If time
- [ ] Play around with different initial agent position distributions on the grid (e.g.: simulate crowds/cities as clusters)
- [ ] Make dynamic lineplot

