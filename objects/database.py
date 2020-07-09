import csv
from constants import constants
from objects.circuit_simulation import CircuitSimulation


class Database:
    ''' Allows to save and load simulations in a csv file, each circuit type 
    is stored in a diferent file to avoid conflict between data an to allow
    future aditions of circtuit types.
    '''

    def __save_low_power_circuit_simulation(self, simulation):
        with open(constants.LOW_POWER_CSV, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow([
                simulation.circuit_operation,
                simulation.approximation_method,
                simulation.bitwidth,
                simulation.approximate_bits,
                simulation.simulation_type,
                simulation.number_of_validations,
                simulation.area,
                simulation.delay,
                simulation.power,
                simulation.pdp,
                simulation.wce,
                simulation.med
            ])

    def save_simulation(self, simulation):
        if simulation.circuit_type == constants.LOW_POWER_CIRCUIT:
            self.__save_low_power_circuit_simulation(simulation)

    def load_simulation(self, simulation):
        pass