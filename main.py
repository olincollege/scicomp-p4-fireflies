from simulation import Simulation

# Define simulation parameters
config = {
    "size": 50, 
    "num_fireflies": 100,
    "num_hours": 9,
    "num_minutes": 3,
    "flashing_threshold": 5,
    "show_fireflies": False
}

# Create and run simulation
sim = Simulation(config)
sim.run()