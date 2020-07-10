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

    def __load_low_power_circuit_simulation(self, simulation):
        simulation_found = False
        with open(constants.LOW_POWER_CSV, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                if simulation.circuit_operation      ==     row[0]  and
                    simulation.approximation_method  ==     row[1]  and
                    simulation.bitwidth              == int(row[2]) and
                    simulation.approximate_bits      == int(row[3]) and
                    simulation.simulation_type       ==     row[4]  and
                    simulation.number_of_validations == int(row[5]):
                    simulation.area  = float(row[6])
                    simulation.delay = float(row[7])
                    simulation.power = float(row[8])
                    simulation.pdp   = float(row[9])
                    simulation.wce   = float(row[10])
                    simulation.med   = float(row[11])
                    simulation_found = True
                    break
        return simulation_found

    def save_simulation(self, simulation):
        if simulation.circuit_type == constants.LOW_POWER_CIRCUIT:
            self.__save_low_power_circuit_simulation(simulation)

    def load_simulation(self, simulation):
        if simulation.circuit_type == constants.LOW_POWER_CIRCUIT:
            return self.__load_low_power_circuit_simulation(simulation)
        else:
            return False