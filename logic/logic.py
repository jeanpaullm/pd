from concurrent.futures import ThreadPoolExecutor
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

    def __simulate(self, simulation):

        if self.design_space_params.database:
            if self.database.load_simulation(simulation):
                self.successful_simulations.append(simulation)
                self.design_space_stats.increment_number_of_loaded_simulations()
                print(f'Loaded  -> {simulation.approximation_method} {simulation.approximate_bits}/{simulation.bitwidth} Validations: {simulation.number_of_validations}')
            else:
                if self.simulator.simulate(simulation):
                    self.successful_simulations.append(simulation)
                    self.database.save_simulation(simulation)
                    self.design_space_stats.increment_number_of_successful_simulations()
                    print(f'Success -> {simulation.approximation_method} {simulation.approximate_bits}/{simulation.bitwidth} Validations: {simulation.number_of_validations}')
                else:
                    self.failed_simulations.append(simulation)
                    self.design_space_stats.increment_number_of_failed_simulations()
                    print(f'Failed  -> {simulation.approximation_method} {simulation.approximate_bits}/{simulation.bitwidth} Validations: {simulation.number_of_validations}')
        else: 
            if self.simulator.simulate(simulation):
                self.successful_simulations.append(simulation)
                self.design_space_stats.increment_number_of_successful_simulations()
                print(f'Success -> {simulation.approximation_method} {simulation.approximate_bits}/{simulation.bitwidth} Validations: {simulation.number_of_validations}')
            else:
                self.failed_simulations.append(simulation)
                self.design_space_stats.increment_number_of_failed_simulations()
                print(f'Failed  -> {simulation.approximation_method} {simulation.approximate_bits}/{simulation.bitwidth} Validations: {simulation.number_of_validations}')
    
    def simulate(self):
        ''' Obtain the charactheristics of a simulation. 

        If database flag is set it looks for the simulation on the database
        if not found simulates it, then append the simulation to the corresponding
        list and updates the stats.
        '''

        if self.design_space_params.threaded:
            with ThreadPoolExecutor(max_workers=4) as executor:
                for simulation in self.total_simulations:
                    executor.submit(self.__simulate,simulation)

        else: 
            for simulation in self.total_simulations:
                self.__simulate(simulation)
            
        

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

        ### print on screen

        print('\n########## Design Space Exploration Finished ##########\n')

        print(f'Database: {self.design_space_params.database}')
        print(f'Threads: {self.design_space_params.threaded}')

        print(f'Circuit Type: {self.design_space_params.circuit_type}')
        print(f'Aritmethic Circuit: {self.design_space_params.circuit_operation}')
        print(f'Bitwidth: {self.design_space_params.bitwidth}')
        print(f'Minimun Approximation: {self.design_space_params.min_approx_bits}')
        print(f'Maximum Approximation: {self.design_space_params.max_approx_bits}')

        print(f'Minimized Charactheristic: {self.design_space_params.charactheristic}')
        print(f'Error Metric: {self.design_space_params.error_metric}')

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
            print(f'  pdp: {solution.pdp}')
            print(f'  med: {solution.med}')
            print(f'  wce: {solution.wce}')
            print('')

        #Print on file


        #Gerenate graphics


        all_errors = []
        all_charactheristics = []
        solution_errors = []
        solution_charactheristics = []


        for simulation in self.successful_simulations:
            if self.design_space_params.error_metric is constants.WCE:
                all_errors.append(simulation.wce)
            else:
                all_errors.append(simulation.med)
            if self.design_space_params.charactheristic is constants.AREA:
                all_charactheristics.append(simulation.area)
            elif self.design_space_params.charactheristic is constants.DELAY:
                all_charactheristics.append(simulation.delay)
            elif self.design_space_params.charactheristic is constants.POWER:
                all_charactheristics.append(simulation.power)    
            else:
                all_charactheristics.append(simulation.pdp)    

        for simulation in self.solutions:
            if self.design_space_params.error_metric is constants.WCE:
                solution_errors.append(simulation.wce)
            else:
                solution_errors.append(simulation.med)
            if self.design_space_params.charactheristic is constants.AREA:
                solution_charactheristics.append(simulation.area)
            elif self.design_space_params.charactheristic is constants.DELAY:
                solution_charactheristics.append(simulation.delay)
            elif self.design_space_params.charactheristic is constants.POWER:
                solution_charactheristics.append(simulation.power)    
            else:
                solution_charactheristics.append(simulation.pdp)  

        pareto_charactheristics, pareto_errors = self.pareto_front( all_charactheristics, all_errors)

        plt.axes()
        plt.axvline(x = self.design_space_params.threshold, linestyle='--')
        plt.plot(all_errors, all_charactheristics, 'k.')
        plt.plot(pareto_errors, pareto_charactheristics, 'rx')
        plt.plot(solution_errors, solution_charactheristics, 'c.')
        plt.xlabel(self.design_space_params.error_metric)
        plt.ylabel(self.design_space_params.charactheristic)
        plt.savefig('result.png')

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
                    for approximate_bits in range(self.design_space_params.min_approx_bits, self.design_space_params.max_approx_bits + 1):
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
        self.simulate()

    def __explore_design_space_brute_force(self):
        """ Searches the simulation that is below the specified error metric threshold
        and has the minimun circuit characteristic and appends it to the 
        """

        for simulation in self.successful_simulations:
                if (
                        (
                            self.design_space_params.error_metric is constants.MED 
                            and simulation.med <= self.design_space_params.threshold
                        )
                        or
                        (
                            self.design_space_params.error_metric is constants.WCE 
                            and simulation.wce <= self.design_space_params.threshold
                        )
                    ):
                    
                    if not self.solutions:
                        self.solutions.append(simulation)
                        self.design_space_stats.increment_number_of_solutions()
                    elif (
                        (
                            self.design_space_params.charactheristic == constants.AREA 
                            and simulation.area < self.solutions[0].area
                        )
                        or
                        (
                            self.design_space_params.charactheristic == constants.DELAY 
                            and simulation.delay < self.solutions[0].delay
                        )
                        or
                        (
                            self.design_space_params.charactheristic == constants.POWER 
                            and simulation.power < self.solutions[0].power
                        )
                        or
                        (
                            self.design_space_params.charactheristic == constants.PDP 
                            and simulation.pdp < self.solutions[0].pdp
                        )
                    ):
                        self.solutions[0] = simulation

    def pareto_front(self, characteristic, error):
        
        pareto_charactheristic = []
        pareto_error = []
        dominated = False

        for (charactheristic1, error1) in zip(characteristic, error):
            for (charactheristic2, error2) in zip(characteristic, error):
                if(
                    (
                        charactheristic2 <= charactheristic1
                        and error2 <= error1
                    )
                    and
                    (    
                        charactheristic2 < charactheristic1
                        or error2 < error1
                    )   
                ):
                    dominated = True
                    break
            if not dominated:
                pareto_charactheristic.append(charactheristic1)
                pareto_error.append(error1)
            else:
                dominated = False

        return pareto_charactheristic, pareto_error