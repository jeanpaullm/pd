
class Simulation:
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
    circuit : Circuit
        circuit object used to abstract the number the type of circuit and his properties
    area: int
        estimated area of the circuit
    delay: int
        estimated delay of the circuit
    power: int
        estimated power of the circuit
    error_rate: int
        error_rate of simulated the circuit
    """

    def __init__(self, approximation_method, simulation_type, number_of_validations, 
                    circuit, area = None, delay = None, power = None, error_rate = None):
        self.approximation_method = approximation_method
        self.simulation_type = simulation_type
        self.number_of_validations = number_of_validations
        self.circuit = circuit
        self.area = area
        self.delay = delay
        self.power = power
        self.error_rate = error_rate

class Circuit:

    def __init__(self, circuit_type, operation, bitwidth):
        self.circuit_type = circuit_type
        self.operation = operation
        self.bitwidth = bitwidth    

class LowPowerCircuit(Circuit):

    def __init__(self, circuit_type, operation, bitwidth, approximate_bits):
        Circuit.__init__(self, circuit_type, operation, bitwidth)
        self.approximate_bits = approximate_bits