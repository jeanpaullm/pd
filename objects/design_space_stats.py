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
        self.number_of_total_simulations = 0
        self.number_of_loaded_simulations = 0
        self.number_of_successful_simulations = 0
        self.number_of_failed_simulations = 0
        self.number_of_solutions = 0

    def start(self):
        self.start_time = datetime.now()

    def finish(self):
        self.finish_time = datetime.now()

    def start_design_space_generation(self):
        self.design_space_generation_time = time.perf_counter()

    def finish_design_space_generation(self):
        self.design_space_generation_time = time.perf_counter() - self.design_space_generation_time

    def start_design_space_exploration(self):
        self.design_space_exploration_time = time.perf_counter()

    def finish_design_space_exploration(self):
        self.design_space_exploration_time = time.perf_counter() - self.design_space_exploration_time

    def increment_number_of_total_simulations(self):
        self.number_of_total_simulations += 1

    def increment_number_of_loaded_simulations(self):
        self.number_of_loaded_simulations += 1

    def increment_number_of_successful_simulations(self):
        self.number_of_successful_simulations += 1

    def increment_number_of_failed_simulations(self):
        self.number_of_failed_simulations += 1 
        
    def increment_number_of_solutions(self):
        self.number_of_solutions += 1