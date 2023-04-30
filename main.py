from simulation import Simulation

# Define simulation parameters
config = {
    "size": 50, 
    "num_fireflies": 10,
    "num_hours": 9,
    "num_minutes": 3
}

# Create and run simulation
sim = Simulation(config)
sim.add_fireflies()
sim.move_fireflies()