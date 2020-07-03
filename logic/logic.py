from constants import constants
from objects.design_space_params import DesignSpaceParams
from objects.design_space_stats import DesignSpaceStats
from objects.circuit_simulation import CircuitSimulationBuilder
from objects.simulator import Simulator

class Logic:
    def __init__(self):
        self.design_space_stats = DesignSpaceStats()
        self.simulator = Simulator()
        self.simulations_to_do = []
        self.simulations_succeeded = []
        self.simulations_failed = []
        self.solutions = []

    def set_ui(self,ui):
        self.ui = ui

    def set_design_space_params(self, design_space_params):
        self.design_space_params = design_space_params

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

        self.design_space_stats.set_design_space_size(len(self.simulations_to_do))
        self.design_space_stats.set_simulations_succeeded(len(self.simulations_succeeded))
        self.design_space_stats.set_simulations_failed(len(self.simulations_failed))
        self.design_space_stats.set_solutions(len(self.solutions))

        print('\n########## Design Space Exploration Finished ##########\n')
        print(f'Design Space Exploration started on: {self.design_space_stats.start_time}')
        print(f'Design Space Exploration finished on: {self.design_space_stats.finish_time}')
        print(f'Generation time: {self.design_space_stats.design_space_generation_time}')
        print(f'Exploration time: {self.design_space_stats.design_space_exploration_time}')
        print('')
        print(f'Desgin space size: {self.design_space_stats.design_space_size}')
        print(f'Succesful simulations: {self.design_space_stats.simulations_succeeded}')
        print(f'Failed simulations: {self.design_space_stats.simulations_failed}')
        print(f'Solutions found: {self.design_space_stats.solutions}')
        print('')
        for solution in self.solutions:
            print('')
            print(f' {solution.approximation_method} {solution.bitwidth} {solution.approximate_bits}')
            print(f'  area: {solution.area}')
            print(f'  delay: {solution.delay}')
            print(f'  power: {solution.power}')
            print('')

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
                        self.simulations_to_do.append(CircuitSimulationBuilder.create_circuit_simulation_low_power(
                            approximation_method, 
                            constants.SYNTHESIS, 
                            number_of_validations, 
                            self.design_space_params.circuit_operation, 
                            self.design_space_params.bitwidth, 
                            approximate_bits
                        ))

        #simulate 
        #fills simulations_succeeded and simulations_failed accordingly 
        for simulation in self.simulations_to_do:
            succesful_simulation = self.simulator.simulate(simulation)
            if succesful_simulation:
                self.simulations_succeeded.append(simulation)
            else:
                self.simulations_failed.append(simulation)

    def __explore_design_space_brute_force(self):
        """ If a speified charachteristic of a given circuit is below the 
         threshold append it to the solutions"""


        # for inside ifs because efficiency

        if self.design_space_params.charactheristic == constants.AREA:
            for simulation in self.simulations_succeeded:
                if simulation.area <= self.design_space_params.threshold:
                    self.solutions.append(simulation)

        elif self.design_space_params.charactheristic == constants.DELAY:
            for simulation in self.simulations_succeeded:
                if simulation.delay <= self.design_space_params.threshold:
                    self.solutions.append(simulation)

        elif self.design_space_params.charactheristic == constants.POWER:
            for simulation in self.simulations_succeeded:
                if simulation.power <= self.design_space_params.threshold:
                    self.solutions.append(simulation)