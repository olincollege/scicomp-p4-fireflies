import numpy as np
import matplotlib.pyplot as plt

from scipy import spatial as sp
from time import time

class Simulation:
    """Simulates a group of fireflies flashing"""
    def __init__(self, config) -> None:
        self.size = config["size"]
        self.num_fireflies = config["num_fireflies"]
        self.num_hours = config["num_hours"]
        self.num_minutes = config["num_minutes"]
        self.flashing_index = self.num_hours*self.num_minutes-1
        self.flashing_threshold = config["flashing_threshold"]
        
        self.frame_count = 0
        self.fireflies = np.zeros((self.num_fireflies, 4))

        plt.ion()

        self.fig = plt.figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111)

    def add_fireflies(self) -> None:
        """Add fireflies at random positions with random internal clocks"""
        # Randomly select position of fireflies
        self.fireflies[:, 0:2] = np.random.randint(low=0, high=self.size, size=(self.num_fireflies, 2))

        # Randomly start internal clocks of fireflies
        self.fireflies[:, 2] = np.random.randint(low=0, high=self.flashing_index, size=self.num_fireflies)
    
    def move_fireflies(self) -> None:
        """Move fireflies in a random direction"""
        directions = np.array([[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]])
        selected_directions = np.random.choice(len(directions), size=self.num_fireflies)        
        self.fireflies[:, 0:2] += directions[selected_directions, :] 
        
        # Correct the position of any firefly that moves off grid
        self.fireflies[:, 0:2][self.fireflies[:, 0:2] < 0] = 0
        self.fireflies[:, 0:2][self.fireflies[:, 0:2] > self.size] = self.size

    def simulate_timestep(self):
        """Flashing and position"""
        # Calculate distances between fireflies
        distances = sp.distance.cdist(self.fireflies[:, 0:2], self.fireflies[:, 0:2])
    
        # Create bitmap of nearby flashing fireflies
        nearby_fireflies = (0 < distances) & (distances <= self.flashing_threshold)
        nearby_flashing_fireflies = nearby_fireflies*self.fireflies[:,3]
        
        # Simplify into 1D array
        nearby_flashing_fireflies = np.any(nearby_flashing_fireflies == 1, axis=1).astype(int)

        # For fireflies that are not near any flashing fireflies, move their internal clock one minute forwards
        is_not_nearby = nearby_flashing_fireflies == 0
        self.fireflies[:, 2][is_not_nearby] += 1
        
        # For fireflies that are near flashing fireflies and not flashing themselves, move their internal clock according to polygon dynamics 
        is_nearby_and_not_flashing = (nearby_flashing_fireflies == 1) & (self.fireflies[:, 2] < self.flashing_index)
        delta = np.floor_divide(self.fireflies[:, 2][is_nearby_and_not_flashing], self.num_minutes)
        self.fireflies[:, 2][is_nearby_and_not_flashing] += delta

        # Reset clocks that have passed the flashing index
        self.fireflies[:, 2][self.fireflies[:, 2] > self.flashing_index] -= self.flashing_index + 1

        # Recount which fireflies are flashing
        self.fireflies[:, 3] = 0
        self.fireflies[:, 3][self.fireflies[:, 2] == self.flashing_index] = 1
        
        # Randomly move all fireflies
        self.move_fireflies()

    def clear_graph(self):
        """Clear graph and set limits"""
        self.ax.clear()
        self.ax.set_xlim([0, self.size])
        self.ax.set_ylim([0, self.size])

    def run(self):
        """Run and plot simulation"""
        # Add fireflies
        self.add_fireflies()

        # Start FPS counter for initial run
        frame_time_start = time()

        while True: 
            ### FLASHING AND POSITION CALCULATIONS ####
            self.simulate_timestep()

            ### PLOTTING ###
            self.clear_graph()

            # Get firefly positions
            x = self.fireflies[:, 0]
            y = self.fireflies[:, 1]

            # Set flashing fireflies to yellow
            colors = np.full(len(self.fireflies), 'blue')
            flashing_firefly_indices = np.where(self.fireflies[:, 3])
            colors[flashing_firefly_indices] = 'red' # TODO: Make array of colors
        
            # Plot fireflies
            self.ax.scatter(x, y, s=5, color=colors)
            
            # Compute and show FPS 
            frame_time_end = time()
            fps = 1 / (frame_time_end - frame_time_start)
            text_fps_string = f'FPS: {fps:.1f}'
            text_fps = self.fig.text(.12, .025, text_fps_string, fontsize=10)

            # Show number of fireflies
            text_num_fireflies_string = f'Fireflies: {self.num_fireflies}'
            text_num_fireflies = self.fig.text(.4, .025, text_num_fireflies_string, fontsize=10)

            # Show number of flashing fireflies
            num_flashing = np.count_nonzero(self.fireflies[:, 3])
            text_num_flashing_string = f'Flashing: {num_flashing}'
            text_num_flashing = self.fig.text(.68, .025, text_num_flashing_string, fontsize=10)

            # DRaw on canvas
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

            # Reset fps timer
            frame_time_start = time()

            # Remove old text
            text_fps.remove()
            text_num_fireflies.remove()
            text_num_flashing.remove()

            self.frame_count += 1


"""
TODO:
-Enable to user to:
    -Adjust the number of fireflies
    -Toggle between whether nudging neighbors adjusts their internal clock
        -Adjust the amount by which their clock gets nudge
        -Adjust how close their neighbor must be in order to be nudged
"""