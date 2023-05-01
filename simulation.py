import numpy as np
import matplotlib.pyplot as plt

from scipy import spatial as sp

"""
TODO:
-Enable user to toggle between whether nudging neighbors adjusts their internal clock
"""

class Simulation:
    """Simulates a group of fireflies flashing"""
    def __init__(self, config) -> None:
        self.size = config["size"]
        self.num_fireflies = config["num_fireflies"]
        self.num_hours = config["num_hours"]
        self.num_minutes = config["num_minutes"]
        self.flashing_index = self.num_hours*self.num_minutes-1
        self.show_fireflies = config["show_fireflies"]
        self.enable_nudging = config["enable_nudging"]
        self.nudging_threshold = config["nudging_threshold"]
        
        self.frame_count = 0
        self.fireflies = np.zeros((self.num_fireflies, 5)) # x, y, clock_position, is_flashing, time_remaining
        self.num_max_flashing = 0

        plt.ion()

        # Initialize plot
        self.fig = plt.figure(figsize=(5, 5), facecolor='black')
        self.ax = self.fig.add_subplot(111, facecolor='black')

    def add_fireflies(self) -> None:
        """Add fireflies at random positions with random internal clocks"""
        # Randomly select position of fireflies
        self.fireflies[:, 0:2] = np.random.randint(low=1, high=self.size, size=(self.num_fireflies, 2))

        # Randomly start internal clocks of fireflies
        self.fireflies[:, 2] = np.random.randint(low=0, high=self.flashing_index, size=self.num_fireflies)
    
    def move_fireflies(self) -> None:
        """Move fireflies in a random direction"""
        directions = np.array([[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]])
        selected_directions = np.random.choice(len(directions), size=self.num_fireflies)        
        self.fireflies[:, 0:2] += directions[selected_directions, :] 
        
        # Correct the position of any firefly that moves off grid
        self.fireflies[:, 0:2][self.fireflies[:, 0:2] < 1] = 1
        self.fireflies[:, 0:2][self.fireflies[:, 0:2] > self.size-1] = self.size-1

    def simulate_timestep(self):
        """Flashing and position"""
        # Record the clock positions of fireflies at the beginning of the timestep
        prev_flashing_fireflies = self.fireflies[:, 3]

        # Decrease the remaining time of all flashing fireflies by one
        self.fireflies[:, 4][prev_flashing_fireflies == 1] -= 1
        self.fireflies[:, 4][self.fireflies[:, 4] < 0] = 0
        
        if self.enable_nudging:
            # Calculate distances between fireflies
            distances = sp.distance.cdist(self.fireflies[:, 0:2], self.fireflies[:, 0:2])

            # Create bitmap of nearby flashing fireflies
            nearby_fireflies = (distances <= self.nudging_threshold)
            nearby_flashing_fireflies = nearby_fireflies*self.fireflies[:,3]

            # Simplify into 1D array
            nearby_flashing_fireflies = np.any(nearby_flashing_fireflies == 1, axis=1).astype(int)

            # For fireflies that are not near any flashing fireflies, move their clock one minute forwards
            is_not_nearby = nearby_flashing_fireflies == 0
            self.fireflies[:, 2][is_not_nearby] += 1
            
            # For fireflies that are near flashing fireflies and not flashing themselves, move their clock according to polygon dynamics 
            is_nearby_and_not_flashing = (nearby_flashing_fireflies == 1) & (self.fireflies[:, 2] < self.flashing_index)
            delta = np.floor_divide(self.fireflies[:, 2][is_nearby_and_not_flashing], self.num_minutes)
            self.fireflies[:, 2][is_nearby_and_not_flashing] += delta + 1
        
        # If at least one new firely has begun flashing, increase the remaining time of all flashing fireflies by one
        curr_flashing_fireflies = (self.fireflies[:, 2] == self.flashing_index).astype(int)
        new_flashing_fireflies = curr_flashing_fireflies - prev_flashing_fireflies
        if np.any(new_flashing_fireflies == 1):
            print("At least one firefly is new")
            self.fireflies[:, 4][curr_flashing_fireflies == 1] += 1
        else:
            print("No new flashing fireflies")

        # For fireflies that are flashing but do not have any remaining time, move their internal clock one minute forwards.
        self.fireflies[:, 2][self.fireflies[:, 4] == 0] += 1
        print(self.fireflies[:, 4])

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

        while True: 
            ### RUN ####
            self.simulate_timestep()

            ### PLOT ###
            self.clear_graph()

            # Get firefly positions
            x = self.fireflies[:, 0]
            y = self.fireflies[:, 1]

            # Set flashing fireflies to yellow
            if self.show_fireflies: 
                color = 'gray'
            else: 
                color = 'k'
            colors = np.full(len(self.fireflies), color)
            flashing_firefly_indices = np.where(self.fireflies[:, 3])
            colors[flashing_firefly_indices] = 'y'
        
            # Plot fireflies
            self.ax.scatter(x, y, s=5, color=colors)

            # Show number of fireflies
            text_num_fireflies_string = f'Fireflies: {self.num_fireflies}'
            text_num_fireflies = self.fig.text(.12, .025, text_num_fireflies_string, fontsize=10, color='white')

            # Show number of flashing fireflies
            num_flashing = np.count_nonzero(self.fireflies[:, 3])
            text_num_flashing_string = f'Flashing: {num_flashing}'
            text_num_flashing = self.fig.text(.4, .025, text_num_flashing_string, fontsize=10, color='white')

            # Show max number of flashing fireflies
            if num_flashing > self.num_max_flashing:
                self.num_max_flashing = num_flashing
            text_num_max_flashing_string = f'Max Flashing: {self.num_max_flashing}'
            text_num_max_flashing = self.fig.text(.68, .025, text_num_max_flashing_string, fontsize=10, color='white')

            # Draw on canvas
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

            # Remove old text
            text_num_fireflies.remove()
            text_num_flashing.remove()
            text_num_max_flashing.remove()

            self.frame_count += 1