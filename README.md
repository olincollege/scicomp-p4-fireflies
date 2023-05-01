# Modeling Synchronous Fireflies
Authored by @mmadanguit (Marion Madanguit).

Python script that models the flashing behavior of synchronized fireflies based on the rules of the flash game laid out in [this paper](https://link.springer.com/article/10.1140/epjs/s11734-021-00397-2). 

Code architecture borrowed from [the Colloid Simulation project](https://github.com/jasperkatzban/colloid-sim) authored by @jasperkaztban (Jasper Katzban). 

## Setup
1. Clone the repository.
2. Run `python3 -m venv venv` and `source venv/bin/activate` to set up and activate a virtual environment.
3. Run `pip install -r requirements.txt` to install the dependencies.

## Customization
In `main.py`, you'll find a few simulation paramters defined in the `config` dictionary:

```
config = {
    "size": 50,                 # Size of simulation grid
    "num_fireflies": 300,       # Number of fireflies in the simulation
    "num_hours": 9,             # Number of sections in the internal clock of the firely
    "num_minutes": 3,           # Number of subsections in the internal clock of the firefly
    "show_fireflies": False,    # Show non-flashing fireflies 
    "enable_nudging": True,     # Enable flashing fireflies to nudge neighboring fireflies
    "nudging_threshold": 1      # Distance neighboring fireflies must be to be nudged
}
```

## Run 
Run `python3 main.py` to run the simulation as configured. 
