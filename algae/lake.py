from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from multivargrid import MultiVarGrid
import seaborn as sns
from fish import Fish
from sim_var import sim_variables

growth_function = sim_variables["growth_function"] 
oxygen_function = sim_variables["oxygen_function"]
algae_value_minimum = sim_variables["algae_value_minimum"]
oxygen_value_minimum = sim_variables["oxygen_value_minimum"]
hunger_rate = sim_variables["hunger_rate"]

class Lake(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, starting_health):
        """Initialize Lake"""
        self.num_agents = N
        self.height = height
        self.width = width
        self.grid= SingleGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        #   Create Grid Storing all Non-Agent Variables
        lake_variables = {'algae' : algae_value_minimum, 'oxygen' : oxygen_value_minimum}
        self.variable_grid = MultiVarGrid(width, height, lake_variables)

        # Create agents
        filled_grids = []
        self.agent_id_cache = []
        for i in range(self.num_agents):
            a = Fish(i, self, starting_health)
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

    def make_oxygen(self, oxygen_func):
        """Add oxygen produced from algae to grid"""
        for y in range(self.height):
            for x in range(self.width):
                algae_value = self.variable_grid.get_value((x,y), 'algae')
                oxygen_value = oxygen_func(algae_value)
                self.variable_grid.add_value((x,y), 'oxygen', oxygen_value) 
                if self.variable_grid.get_value((x,y), 'oxygen') > 1:
                    self.variable_grid.change_value((x,y), 'oxygen', 1)

    def create_new_agent(self, pos, starting_health):
        """Create new Fish Agent"""
        agent_id = self.agent_id_cache[-1] + 1
        a = Fish(agent_id, self, starting_health)
        self.schedule.add(a)
        self.agent_id_cache.append(agent_id)
        self.grid.place_agent(a, pos)
        
    def step(self):
        self.variable_grid.growth_grid('algae', growth_function) 
        self.make_oxygen(oxygen_function)
        self.schedule.step()
        self.display_variables()

    def display_variables(self):
        algae_grid = self.variable_grid.return_variable_grid('algae')
        oxygen_grid = self.variable_grid.return_variable_grid('oxygen')

        #   Rotate Grid 3 times
        for i in range(3):
            algae_grid = list(zip(*algae_grid[::-1])) 
            oxygen_grid = list(zip(*oxygen_grid[::-1]))

        ax_algae = sns.heatmap(algae_grid, annot=False, cmap='Greens', cbar = False)
        fig_algae = ax_algae.get_figure()
        fig_algae.savefig("liveview/algae.jpg")
    
        ax_oxygen = sns.heatmap(oxygen_grid, annot=False, cmap='vlag', cbar = False)
        fig_oxygen = ax_oxygen.get_figure()
        fig_oxygen.savefig("liveview/oxygen.jpg")

