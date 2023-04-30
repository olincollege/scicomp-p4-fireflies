from simulation import Simulation

# Define simulation parameters
config = {
    "size": 50, 
    "num_fireflies": 300,
    "num_hours": 9,
    "num_minutes": 3,
    "flashing_threshold": 10
}

# Create and run simulation
sim = Simulation(config)
sim.run()