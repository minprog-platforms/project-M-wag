from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from multivargrid import MultiVarGrid
import seaborn as sns
import matplotlib.pyplot as plt
from fish import Fish
from math import atan, pi

growth_function = lambda x : -0.33/pi*atan(x - 1)
oxygen_function = lambda x : 0.3*(-x + 1.2)

class Lake(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, starting_health, hunger_rate):
        self.num_agents = N
        self.grid= SingleGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.height = height
        self.width = width
        self.hunger_rate = hunger_rate
        #   Create Grid Storing all Non-Agent Variables
        lake_variables = {'algae' : 0.0, 'oxygen' : 0.7}
        self.variable_grid = MultiVarGrid(width, height, lake_variables)

        # Create agents
        filled_grids = []
        self.agent_id_cache = []
        for i in range(self.num_agents):
            a = Fish(i, self, starting_health, hunger_rate)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                if (x,y) not in filled_grids:
                    filled_grids.append((x,y))
                    self.grid.place_agent(a, (x, y))
                    agent_scheduler_id = i 
                    self.agent_id_cache.append(agent_scheduler_id)
                    break

    def create_new_agent(self, pos, starting_health):
        agent_id = self.agent_id_cache[-1] + 1
        a = Fish(agent_id, self, starting_health, self.hunger_rate)
        self.schedule.add(a)
        self.agent_id_cache.append(agent_id)
        self.grid.place_agent(a, pos)
        
    def step(self):
        self.variable_grid.growth_grid('algae', growth_function) 
        self.variable_grid.make_oxygen(oxygen_function)
        self.schedule.step()
        self.display_variables()

    def display_variables(self):
        algae_grid = self.variable_grid.return_variable_grid('algae')
        oxygen_grid = self.variable_grid.return_variable_grid('oxygen')

        fish_grid = []
        for w in range(self.width):
            col = []
            for h in range(self.height):
                grid_content = self.grid.grid[w][h]
                if grid_content == None:
                    fish_health = 0
                else:
                    fish_health = grid_content.health
                col.append(fish_health) 
            fish_grid.append(col)

        #   Rotate Grid 3 times
        for i in range(3):
            algae_grid = list(zip(*algae_grid[::-1])) 
            oxygen_grid = list(zip(*oxygen_grid[::-1]))
            fish_grid = list(zip(*fish_grid[::-1]))

        ax_algae = sns.heatmap(algae_grid, annot=False, cmap='Greens', cbar = False)
        fig_algae = ax_algae.get_figure()
        fig_algae.savefig("liveview/algae.jpg")
    
        ax_oxygen = sns.heatmap(oxygen_grid, annot=False, cbar = False)
        fig_oxygen = ax_oxygen.get_figure()
        fig_oxygen.savefig("liveview/oxygen.jpg")

        #   Print Grid
        for i in range(0, self.height):
            print(["{:.2f}".format(number) for number in algae_grid[i]], end='\t')
            print(["{:.2f}".format(number) for number in oxygen_grid[i]], end = '\t')
            print(["{:.2f}".format(number) for number in fish_grid[i]])
