from constants import constants

class CircuitSimulation:
    """
    Represents the simulation, initialy is used to store the simulation parameters,
    such as  approximation_methos, simulation_type, number_of_validations and circuit 
    properties, after the simulation data is obtained and stored in the respective atributes
    

    Attributes
    ----------
    approximation_method : str
        the approximation methos used to approximate the circuit ex: AXA, LOA, AMA..
    simulation_type : str
        simulation used to characterize the circuit ex: syn, postsyn, ...
    number_of_validations : int
        number of results used to calculate the accuracy of the circuit.
    circuit_type : str
        type of circuit to be simulated
    circuit_operation : str
        type of circuit arithmethic simulation to be simulated
    bitwidth : int
        bitwidth of the simulated circuits
    area: int
        estimated area of the circuit
    delay: int
        estimated delay of the circuit
    power: int
        estimated power of the circuit
    error_rate: int
        error_rate of simulated the circuit
    """

    def __init__(self, 
                 approximation_method, 
                 simulation_type, 
                 number_of_validations, 
                 circuit_type, 
                 circuit_operation,
                 bitwidth, 
                 area = None, 
                 delay = None, 
                 power = None, 
                 error_rate = None):
        self.approximation_method = approximation_method
        self.simulation_type = simulation_type
        self.number_of_validations = number_of_validations
        self.circuit_type = circuit_type
        self.circuit_operation = circuit_operation
        self.bitwidth = bitwidth    
        self.area = area
        self.delay = delay
        self.power = power
        self.error_rate = error_rate

class LowPowerCircuitSimulation(CircuitSimulation):
    """
    Extends CircuitSimulation. Represents a low power circuit simulation.
    

    Attributes
    ----------
    approximate_bits : int
        Number of bits aproximated in the circuit to be simulated
    """
    def __init__(self, 
                 approximation_method, 
                 simulation_type,
                 number_of_validations,
                 circuit_operation,
                 bitwidth,
                 approximate_bits):
        CircuitSimulation.__init__(self,
                                   approximation_method,
                                   simulation_type,
                                   number_of_validations,
                                   constants.LOW_POWER_CIRCUIT,
                                   circuit_operation, 
                                   bitwidth)
        self.approximate_bits = approximate_bits 

class CircuitSimulationBuilder():
    """
    Used to encapsulate the creation objects that extends CircuitSimulation
    """

    @staticmethod
    def create_circuit_simulation_low_power(approximation_method, 
                                            simulation_type,
                                            number_of_validations, 
                                            circuit_operation,
                                            bitwidth,
                                            approximate_bits):

        """
        Static method used to create LowPowerCircuits

        Parameters
        ----------
        approximation_method : str
            the approximation methos used to approximate the circuit ex: AXA, LOA, AMA..
        simulation_type : str
            simulation used to characterize the circuit ex: syn, postsyn, ...
        number_of_validations : int
            number of results used to calculate the accuracy of the circuit.
        circuit_operation : str
            type of circuit arithmethic simulation to be simulated
        bitwidth : int
            bitwidth of the simulated circuits
        approximate_bits : int
            Number of bits aproximated in the circuit to be simulated
        """
        return LowPowerCircuitSimulation(approximation_method,
                               simulation_type,
                               number_of_validations, 
                               circuit_operation,
                               bitwidth,
                               approximate_bits)  