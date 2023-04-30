from simulation import Simulation

# Define simulation parameters
config = {
    "size": 5, 
    "num_fireflies": 5,
    "num_sides": 9,
    "max_time": 100
}

# Create and run simulation
sim = Simulation(config)
sim.add_fireflies()