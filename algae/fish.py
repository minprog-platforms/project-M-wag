from matplotlib.style import available
from mesa import Agent
from copy import deepcopy
import random

from typing import (
    Tuple,
    List
)

Coordinate = Tuple[int, int]
max_intake = 0.3
birth_threshold = 0.8
birth_cost = 0.3

class Fish(Agent):
    def __init__(self, unique_id, model, starting_health, hunger_rate) -> None:
        super().__init__(unique_id, model)
        self.health= starting_health
        self.hunger_rate = hunger_rate
        self.living = True

    
    def step(self) -> None:
        self.health-= self.hunger_rate 

        oxygen_level =  self.model.variable_grid.get_value(self.pos, 'oxygen')
        if oxygen_level < 0.5:
            self.health -= (0.5 - oxygen_level)/2
        self.model.variable_grid.add_value(self.pos, 'oxygen', -0.1)
        if oxygen_level - 0.1 < 0:
            self.model.variable_grid.change_value(self.pos, 'oxygen', 0)

        if self.health > birth_threshold and len(self.get_free_space(can_move_center = False)) > 0:
            self.birth()
        if self.health <= 0.0:
            self.die()
            return

        self.move_to_food()
        if self.check_for_food():
             self.eat()

    def move(self, new_position) -> None:
        self.model.grid.move_agent(self ,new_position)

    def move_to_food(self) -> None:
        """Locate the nearest source of food and move towards it"""
        new_position = self.locate_food()
        self.move(new_position)

    def get_free_space(self, can_move_center: bool) -> List[Coordinate]:
        """Get coords for availabe space"""
        surrounding_coords = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=can_move_center) 
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False) 

        neighbor_coords = [neighbor.pos for neighbor in neighbors]
        free_space = list(set(surrounding_coords).symmetric_difference(neighbor_coords))

        return free_space

    def locate_food(self) -> Coordinate:
        """Move to location based on food density"""
        free_space = self.get_free_space(can_move_center = True)
        #   Get algae density of surrounding cells
        algae_grid = deepcopy(self.model.variable_grid.return_variable_grid('algae'))
        free_space_algae_value = [algae_grid[coord[0]][coord[1]] for coord in free_space]

        next_move = random.choices(free_space, free_space_algae_value)
        next_move = next_move[0]

        return next_move

    def check_for_food(self):
        """Check whether current cell has algae"""
        algae_grid = deepcopy(self.model.variable_grid.return_variable_grid('algae'))
        current_cell_algae_value = algae_grid[self.pos[0]][self.pos[1]]
        if current_cell_algae_value > 0:
            return True
        else:
            return False

    def eat(self):
        """Consume a patch of algae"""
        eatable_algae = self.calculate_food_intake() 
        self.health += eatable_algae
        self.model.variable_grid.add_value(self.pos, 'algae', -1 * eatable_algae)

    def calculate_food_intake(self) -> float:
        """Gauge how much algae can be consumed""" 
        # If Full Don't Eat
        if self.health >= 1.0:
            available_intake = 0
            return available_intake 
        # Never eat more then max health
        intake_to_full_health = 1 - self.health
        # Never eat more algae then possible
        available_algae = self.model.variable_grid.get_value(self.pos, "algae")
        
        #   Can never eat more algae then available
        #   Can never eat more then max intake
        #   Can never eat more then max health
        if available_algae > intake_to_full_health:
            available_intake = intake_to_full_health
        else:
            available_intake = available_algae
        
        if available_intake > max_intake:
            available_intake = max_intake

        return available_intake

    def die(self):
        self.living = False
        self.model.schedule.remove(self)
        
    def birth(self):
        self.health -= birth_cost
        birth_pos = random.choice(self.get_free_space(can_move_center = False))
        self.model.create_new_agent(birth_pos, birth_cost)
        