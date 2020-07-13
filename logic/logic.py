import matplotlib.pyplot as plt
from constants import constants
from objects.design_space_params import DesignSpaceParams
from objects.design_space_stats import DesignSpaceStats
from objects.circuit_simulation import CircuitSimulationBuilder
from objects.simulator import Simulator
from objects.database import Database

class Logic:
    def __init__(self):
        self.design_space_stats = DesignSpaceStats()
        self.simulator = Simulator()
        self.database = Database()
        self.total_simulations = []
        self.successful_simulations = []
        self.failed_simulations = []
        self.solutions = []

    def set_ui(self,ui):
        self.ui = ui

    def set_design_space_params(self, design_space_params):
        self.design_space_params = design_space_params

    def simulate(self, simulation):
        ''' Obtain the charactheristics of a simulation. 

        If database flag is set it looks for the simulation on the database
        if not found simulates it, then append the simulation to the corresponding
        list and updates the stats.
        '''
        if self.database.load_simulation(simulation): #add database flag check
                self.successful_simulations.append(simulation)
                self.design_space_stats.increment_number_of_loaded_simulations()
                print("data retrieved from database")
        else: 
            if self.simulator.simulate(simulation):
                self.successful_simulations.append(simulation)
                self.database.save_simulation(simulation)
                self.design_space_stats.increment_number_of_successful_simulations()
            else:
                self.failed_simulations.append(simulation)
                self.design_space_stats.increment_number_of_failed_simulations()

    def init(self):
        '''
        executes and generates design space, keeps track of time 
        taken and multiple simulation stats by means of the 
        design_space_stats
        '''
        self.design_space_stats.start()

        self.design_space_stats.start_design_space_generation()
        self.__generate_design_space_brute_force()
        self.design_space_stats.finish_design_space_generation()

        self.design_space_stats.start_design_space_exploration()
        self.__explore_design_space_brute_force()
        self.design_space_stats.finish_design_space_exploration()

        self.design_space_stats.finish()

        ### REFACTORIZAR ###

        print('\n########## Design Space Exploration Finished ##########\n')
        print(f'Design Space Exploration started on: {self.design_space_stats.start_time}')
        print(f'Design Space Exploration finished on: {self.design_space_stats.finish_time}')
        print(f'Generation time: {self.design_space_stats.design_space_generation_time}')
        print(f'Exploration time: {self.design_space_stats.design_space_exploration_time}')
        print('')
        print(f'Desgin space size: {self.design_space_stats.number_of_total_simulations}')
        print(f'Loaded simulations: {self.design_space_stats.number_of_loaded_simulations}')
        print(f'Succesful simulations: {self.design_space_stats.number_of_successful_simulations}')
        print(f'Failed simulations: {self.design_space_stats.number_of_failed_simulations}')
        print(f'Solutions found: {self.design_space_stats.number_of_solutions}')
        print('')
        for solution in self.solutions:
            print('')
            print(f' {solution.approximation_method} {solution.bitwidth} {solution.approximate_bits}')
            print(f'  area: {solution.area}')
            print(f'  delay: {solution.delay}')
            print(f'  power: {solution.power}')
            print(f'  med: {solution.med}')
            print(f'  wce: {solution.wce}')
            print('')

        errors = []
        charactheristics = []

        for simulation in self.successful_simulations:
            if self.design_space_params.error_metric is constants.WCE:
                errors.append(simulation.wce)
            else:
                errors.append(simulation.med)
            if self.design_space_params.error_metric is constants.AREA:
                charactheristics.append(simulation.area)
            elif self.design_space_params.error_metric is constants.DELAY:
                charactheristics.append(simulation.delay)
            elif self.design_space_params.error_metric is constants.POWER:
                charactheristics.append(simulation.power)    
            else:
                charactheristics.append(simulation.pdp)    

        plt.plot(errors, charactheristics, 'ro')
        plt.xlabel(self.design_space_params.error_metric)
        plt.ylabel(self.design_space_params.charactheristic)
        plt.show()

    def __generate_design_space_brute_force(self):
        """ Given the design_space_params fills the simulations array with the 
        simulations to be done"""

        number_of_validations = 0

        if self.design_space_params.bitwidth < 20: #if 20 of grather num of validations becomes to big
            number_of_validations = 2 ** self.design_space_params.bitwidth

        else:
            number_of_validations = 1000000 

        # generate circuits to be generated
        if self.design_space_params.circuit_type == constants.LOW_POWER_CIRCUIT:
            if self.design_space_params.circuit_operation == constants.ADDER:
                for approximation_method in constants.LOW_POWER_ADDERS:
                    for approximate_bits in range(self.design_space_params.min_approx_bits, self.design_space_params.max_approx_bits):
                        self.total_simulations.append(CircuitSimulationBuilder.create_circuit_simulation_low_power(
                            approximation_method, 
                            constants.SYNTHESIS, 
                            number_of_validations, 
                            self.design_space_params.circuit_operation, 
                            self.design_space_params.bitwidth, 
                            approximate_bits
                        ))
                        self.design_space_stats.increment_number_of_total_simulations()

        #simulate 
        for simulation in self.total_simulations:
            self.simulate(simulation)

    def __explore_design_space_brute_force(self):
        """ If a specified error metric of a given circuit is below the 
         threshold append it to the solutions"""

        '''

        # for inside ifs because efficiency

        if self.design_space_params.charactheristic == constants.AREA:
            for simulation in self.successful_simulations:
                if simulation.area <= self.design_space_params.threshold:
                    self.solutions.append(simulation)

        elif self.design_space_params.charactheristic == constants.DELAY:
            for simulation in self.successful_simulations:
                if simulation.delay <= self.design_space_params.threshold:
                    self.solutions.append(simulation)

        elif self.design_space_params.charactheristic == constants.POWER:
            for simulation in self.successful_simulations:
                if simulation.power <= self.design_space_params.threshold:
                    self.solutions.append(simulation)

        elif self.design_space_params.charactheristic == constants.PDP:
            for simulation in self.successful_simulations:
                if simulation.pdp <= self.design_space_params.threshold:
                    self.solutions.append(simulation)   

        '''

        if self.design_space_params.error_metric == constants.MED:
            for simulation in self.successful_simulations:
                if simulation.med <= self.design_space_params.threshold:
                    self.solutions.append(simulation)
                    self.design_space_stats.increment_number_of_solutions()

        elif self.design_space_params.error_metric == constants.WCE:
            for simulation in self.successful_simulations:
                if simulation.wce <= self.design_space_params.threshold:
                    self.solutions.append(simulation)
                    self.design_space_stats.increment_number_of_solutions()