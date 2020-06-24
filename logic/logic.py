from constants import constants
from objects.design_space_params import DesignSpaceParams
from objects.design_space_stats import DesignSpaceStats
from objects.circuit_simulation import CircuitSimulationBuilder
from objects.simulator import Simulator

class Logic:
    def __init__(self):
        self.design_space_stats = DesignSpaceStats()
        self.simulator = Simulator()
        self.simulations = []
        self.solutions = []

    def set_ui(self,ui):
        self.ui = ui

    def set_design_space_params(self, design_space_params):
        self.design_space_params = design_space_params

    def init(self):
        #ver que con los timmers
        self.__generate_design_space_brute_force()
        self.__explore_design_space_brute_force()
        #ver que con los timmer


    def __generate_design_space_brute_force(self):
        """ Given the design_space_params fills the simulations array with the 
        simulations to be done"""

        number_of_validations = 0

        if self.design_space_params.bitwidth < 20:
            number_of_validations = self.design_space_params.bitwidth ^ 2

        else:
            number_of_validations = 1000000 

        # generate circuits to be generated
        if self.design_space_params.circuit_type == constants.LOW_POWER_CIRCUIT:
            if self.design_space_params.circuit_operation == constants.ADDER:
                for approximation_method in constants.LOW_POWER_ADDERS:
                    for approximate_bits in range(self.design_space_params.min_approx_bits, self.design_space_params.max_approx_bits):
                        self.simulations.append(CircuitSimulationBuilder.create_circuit_simulation_low_power(
                            approximation_method, 
                            constants.SYNTHESIS, 
                            number_of_validations, 
                            self.design_space_params.circuit_operation, 
                            self.design_space_params.bitwidth, 
                            approximate_bits
                        ))

        self.design_space_stats.simulations = len(self.simulations)

        #simulate 

        for simulation in self.simulations:
            self.simulator.simulate(simulation)

    def __explore_design_space_brute_force(self):
        """ If a speified charachteristic of a given circuit is below the 
         threshold append it to the solutions"""


        # for inside ifs because efficiency

        if self.design_space_params.charactheristic == constants.AREA:
            for simulation in self.simulations:
                if simulation.area <= self.design_space_params.threshold:
                    self.solutions.append(simulation)

        elif self.design_space_params.charactheristic == constants.DELAY:
            for simulation in self.simulations:
                if simulation.delay <= self.design_space_params.threshold:
                    self.solutions.append(simulation)

        elif self.design_space_params.charactheristic == constants.POWER:
            for simulation in self.simulations:
                if simulation.power <= self.design_space_params.threshold:
                    self.solutions.append(simulation)