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
        self.pareto_front_simulations = []
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
        print('')
        print(f'Circuit Type: {self.design_space_params.circuit_type}')
        print(f'Aritmethic Circuit: {self.design_space_params.circuit_operation}')
        print(f'Bitwidth: {self.design_space_params.bitwidth}')
        print(f'Minimun Approximation: {self.design_space_params.min_approx_bits}')
        print(f'Maximum Approximation: {self.design_space_params.max_approx_bits}')
        print(f'Minimized Charactheristic: {self.design_space_params.charactheristic}')
        print(f'Error Metric: {self.design_space_params.error_metric}')
        print('')
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

        f = open("log.txt", "a")
        f.write('\n########## Design Space Exploration Finished ##########\n')
        f.write(f'Database: {self.design_space_params.database}\n')
        f.write(f'Threads: {self.design_space_params.threaded}\n\n')
        f.write(f'Circuit Type: {self.design_space_params.circuit_type}\n')
        f.write(f'Aritmethic Circuit: {self.design_space_params.circuit_operation}\n')
        f.write(f'Bitwidth: {self.design_space_params.bitwidth}\n')
        f.write(f'Minimun Approximation: {self.design_space_params.min_approx_bits}\n')
        f.write(f'Maximum Approximation: {self.design_space_params.max_approx_bits}\n\n')
        f.write(f'Minimized Charactheristic: {self.design_space_params.charactheristic}\n')
        f.write(f'Error Metric: {self.design_space_params.error_metric}\n\n')
        f.write(f'Design Space Exploration started on: {self.design_space_stats.start_time}\n')
        f.write(f'Design Space Exploration finished on: {self.design_space_stats.finish_time}\n')
        f.write(f'Generation time: {self.design_space_stats.design_space_generation_time}\n')
        f.write(f'Exploration time: {self.design_space_stats.design_space_exploration_time}\n\n')
        f.write(f'Desgin space size: {self.design_space_stats.number_of_total_simulations}\n')
        f.write(f'Loaded simulations: {self.design_space_stats.number_of_loaded_simulations}\n')
        f.write(f'Succesful simulations: {self.design_space_stats.number_of_successful_simulations}\n')
        f.write(f'Failed simulations: {self.design_space_stats.number_of_failed_simulations}\n')
        f.write(f'Solutions found: {self.design_space_stats.number_of_solutions}\n')
        for solution in self.solutions:
            f.write(f'  {solution.approximation_method} {solution.bitwidth} {solution.approximate_bits}')
            f.write(f' area: {solution.area}')
            f.write(f' delay: {solution.delay}')
            f.write(f' power: {solution.power}')
            f.write(f' pdp: {solution.pdp}')
            f.write(f' med: {solution.med}')
            f.write(f' wce: {solution.wce}')
        f.close()

        #Gerenate graphics
        all_errors = []
        all_charactheristics = []
        solution_errors = []
        solution_charactheristics = []
        pareto_errors = []
        pareto_charactheristics = []

        for simulation in self.successful_simulations:
            all_errors.append(getattr(simulation, self.design_space_params.error_metric))
            all_charactheristics.append(getattr(simulation, self.design_space_params.charactheristic))

        for simulation in self.solutions:
            solution_errors.append(getattr(simulation, self.design_space_params.error_metric))
            solution_charactheristics.append(getattr(simulation, self.design_space_params.charactheristic))

        for simulation in self.pareto_front_simulations:
            pareto_errors.append(getattr(simulation, self.design_space_params.error_metric))
            pareto_charactheristics.append(getattr(simulation, self.design_space_params.charactheristic))

        plt.axes()
        plt.xscale('symlog')
        plt.grid(True)
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

        self.generate_pareto_front()

        for simulation in self.pareto_front_simulations:
            if(getattr(simulation, self.design_space_params.error_metric) <= self.design_space_params.threshold):
                if not self.solutions:
                    self.solutions.append(simulation)
                    self.design_space_stats.increment_number_of_solutions()
                elif(getattr(simulation, self.design_space_params.charactheristic) < getattr(self.solutions[0],self.design_space_params.charactheristic)):
                    self.solutions[0] = simulation

    def generate_pareto_front(self):

        dominated = False

        for simulation1 in self.successful_simulations:
            for simulation2 in self.successful_simulations:
                if(
                    (
                        getattr(simulation2, self.design_space_params.charactheristic) <= getattr(simulation1, self.design_space_params.charactheristic) 
                        and getattr(simulation2, self.design_space_params.error_metric) <= getattr(simulation1, self.design_space_params.error_metric)
                    )
                    and
                    (    
                        getattr(simulation2, self.design_space_params.charactheristic) < getattr(simulation1, self.design_space_params.charactheristic) 
                        or getattr(simulation2, self.design_space_params.error_metric) < getattr(simulation1, self.design_space_params.error_metric)
                    )   
                ):
                    dominated = True
                    break

            if not dominated:
                self.pareto_front_simulations.append(simulation1)
            else:
                dominated = False