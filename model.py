import random
import numpy as np

class Firefly:
    """Represents a single firefly"""
    def __init__(self, position):
        self.position = position # Current position
        self.remaining_time = 0 # Remaining time in the box
        
    def move(self, n_sides):
        """Updates the firefly's position according to the polygon dynamics"""
        # TODO: Move each firefly forward according to the number of sides of the polygon, e.g. when a firefly is is on a box on the first side, it advances one position.
        
    def flash(self): 
        """Indicates that the firefly has flashed"""
        print(f"Firefly at position {self.position} flashing")
        
    def decrement_time(self):
        """Reduces the remaining time in the flashing box by 1"""
        self.remaining_time = max(0, self.remaining_time - 1)
        
    def set_time(self, time):
        """Sets the remaining time in the flashing box to a given value"""
        self.remaining_time = time

def simulate_fireflies(num_fireflies, n_sides, flashing_box_index, max_time):
    """Simulates a group of fireflies and their movements for a given number of time steps. 
    Returns a 2D array indicated when each firefly flashed at each timestep"""
    fireflies = [Firefly(i) for i in range(num_fireflies) if i != flashing_box_index] # Create a list of Firefly objects for all firefles except the flashing box
    flashes = np.zeros((num_fireflies, max_time)) # Create an array to record the fireflies that flash at each timestep
    for t in range(max_time): 
        pass
        # If no fireflies are in the flashing box, move each firefly one position forward
        # If there is a firefly in the flashing box, it stays in the flashing box for one time step and each firefly moves forward according to the number of sides of the polygon.
        
    return flashes

"""
TODO:
-Finish implementing simulate_fireflies
-Visualize fireflies flashing
-Make fireflies position dynamic
-Enable to user to:
    -Adjust the number of fireflies
    -Toggle between whether nudging neighbors adjusts their internal clock
        -Adjust the amount by which their clock gets nudge
        -Adjust how close their neighbor must be in order to be nudged
"""

if __name__ == '__main__':

    flashes = simulate_fireflies(num_fireflies=5, n_sides=5, flashing_box_index=4, max_time=100)
    print(flashes)