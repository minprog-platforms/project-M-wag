from lake import Lake
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def main():
    dim = 10
    var = {
        "N" : 1,
        "width" : dim,
        "height" : dim,
        "starting_health" : 0.5,
        "hunger_rate" : 0.4,
    }

#   Everything below here should stay unchanged

    grid = CanvasGrid(agent_portrayal, var["width"], var["height"], 500, 500)
    server = ModularServer(Lake,
                        [grid],
                        "Lake Model",
                        {"N":1, "width": var["width"], "height":var["height"], "starting_health" : 0.5})
    server.port = 8521 
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