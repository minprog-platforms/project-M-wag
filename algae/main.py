from lake import Lake
from fish import Fish
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def main():
    dim = 3
    grid = CanvasGrid(agent_portrayal, dim, dim, 500, 500)
    server = ModularServer(Lake,
                        [grid],
                        "Lake Model",
                        {"N":1, "width":dim, "height":dim, "starting_health" : 0.5, "hunger_rate": 0.1 })
    server.port = 8521 # The default
    server.launch()

def agent_portrayal(agent):
    
    portrayal = {"Shape": "circle",
                "Filled": "true",
                "Layer": 0,
                "Color": "red",
                "r" : 0.5
                }
    
    if agent.living == False:
        portrayal["r"] = 0.0
    return portrayal

main()