from math import atan, pi


# default_variables = {
#     "birth_threshold" : 0.85,
#     "birth_cost" : 0.3,
#     "max_algae_intake" : 0.2,
#     "oxygen_intake" : 0.3,
#     "suffocation_threshold" : 0.5,
#     "oxygen_damage_func" : lambda x: x/1.2,
#     "hunger_rate" : 0.1,
#     "growth_function" : lambda x : -0.23/pi*atan(x - 1.1),
#     "oxygen_function" : lambda x : 0.3*(-x + 1.1),
#     "algae_value_minimum" : 0,
#     "oxygen_value_minimum" : 0.7,
# }

sim_variables = {
    "birth_threshold" : 0.85,
    "birth_cost" : 0.3,
    "max_algae_intake" : 0.2,
    "oxygen_intake" : 0.3,
    "suffocation_threshold" : 0.5,
    "oxygen_damage_func" : lambda x: x/1.2,
    "hunger_rate" : 0.1,
    "growth_function" : lambda x : -0.23/pi*atan(x - 1.1),
    "oxygen_function" : lambda x : 0.3*(-x + 1.1),
    "algae_value_minimum" : 0,
    "oxygen_value_minimum" : 0.7
}