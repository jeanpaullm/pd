import time
from datetime import datetime

class DesignSpaceStats:

    """
    Class used to keep record of the stats from the generation and exploration
    of the designs space


    Attributes
    ----------
    start_time : datetime
        time and date in which the execution of the program started
    finish_time : datetime
        time and date in which the execution of the program finished
    design_space_generation_time : int
        seconds the design space generation was executed
    design_space_exploration_time : int
        seconds the design space exploration was executed
    design_space_size : int
        design space size number
    recovered_from_database : int
        number of simulations retrieved from database
    simulations_done : int
        number of successful simulations
    simulations_failed : int
        number of failed simulations
    solutions : int
        number of solutions found

    """

    def __init__(self):
        self.start_time = None
        self.finish_time = None
        self.design_space_generation_time = 0
        self.design_space_exploration_time = 0
        self.design_space_size = None
        self.recovered_from_database = 0
        self.simulations_done = 0
        self.simulation succeeded = 0
        self.simulations_failed = 0
        self.solutions = 0

    def start(self):
        self.start_time = datetime.now()

    def finish(self):
        self.stop_time = datetime.now()

    def start_design_space_generation(self):
        self.design_space_generation_time = time.perf_counter()

    def finish_design_space_generation(self):
        self.design_space_generation_time = time.perf_counter() - self.design_space_generation_time

    def start_design_space_exploration(self):
        self.design_space_exploration_time = time.perf_counter()

    def finish_design_space_exploration(self):
        self.design_space_exploration_time = time.perf_counter() - self.design_space_exploration_time

    def set_design_space_size(self, design_space_size):
        self.design_space_size = design_space_size

    def set_simuations_succeeded(self, simulations_succeeded):
        self.simulations_succeeded = simulations_succeeded

    def set_simuations_failed(self, simulations_failed):
        self.simulations_failed = simulations_failed

    def set_solutions(self, solutions):
        self.solutions = solutions