from multivargrid import MultiVarGrid
from fish import Fish
from mesa.model import Model
from mesa.time import RandomActivation

class LakeModel(Model):
    def __init__(self, N, width, height, agent_variant):
        self.num_agents = N
        self.grid = MultiVarGrid(width, height, True)
        self.schedule = RandomActivation(self) 

        agent_variant = "Normal"
        # Populate with agents
        for i in range(self.num_agents):
            a = {"Fish" : Fish(i, self, agent_variant)}
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

       