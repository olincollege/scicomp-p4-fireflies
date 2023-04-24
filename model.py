import random

class Firefly:
    """Represents a single firefly."""
    def __init__(self, position, internal_clock):
        self.position = position
        self.internal_clock = internal_clock
        
    def flash(self):
        """Prints a message indiciating that the firefly has flashed at the current time."""
        print(f"Firefly {self.position} flashing at time {self.internal_clock}")
        
    def nudge_clock(self, amount):
        """Adds a small amount to the firefly's internal clock."""
        self.internal_clock += amount

def simulate_fireflies(num_fireflies, max_time, nudge_amount):
    """Stimulate a group of fireflies."""
    fireflies = [Firefly(i, random.randint(1, max_time)) for i in range(num_fireflies)] # Create a list of Firefly objects with random internal clocks
    for t in range(1, max_time+1): # Loop through each time step from 1 to max_time
        for i in range(num_fireflies): 
            if fireflies[i].internal_clock % 12 == 0: # At each time step, check if any firefly's internal clock has reached the designated flashing time, in this case 12
                fireflies[i].flash() 
                for j in range(num_fireflies): # Check for nearby fireflies that should be nudged
                    if i != j and abs(fireflies[i].position - fireflies[j].position) == 1:
                        fireflies[j].nudge_clock(nudge_amount) 

"""
TODO:
-Visualize fireflies flashing
-Make fireflies position dynamic
-Enable to user to:
    -Adjust the number of fireflies
    -Toggle between whether nudging neighbors adjusts their internal clock
        -Adjust the amount by which their clock gets nudge
        -Adjust how close their neighbor must be in order to be nudged
"""

if __name__ == '__main__':

    simulate_fireflies(num_fireflies=5, max_time=100, nudge_amount=1)