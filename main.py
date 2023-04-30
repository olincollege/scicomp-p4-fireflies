from simulation import Simulation

# Define simulation parameters
config = {
    "size": 5, 
    "num_fireflies": 4,
    "num_hours": 9,
    "num_minutes": 3
}

# Create and run simulation
sim = Simulation(config)
sim.add_fireflies()