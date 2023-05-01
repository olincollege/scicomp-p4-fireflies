from simulation import Simulation

# Define simulation parameters
config = {
    "size": 50, 
    "num_fireflies": 300,
    "num_hours": 9,
    "num_minutes": 3,
    "show_fireflies": False,
    "enable_nudging": True,
    "nudging_threshold": 1
}

# Create and run simulation
sim = Simulation(config)
sim.run()