from constants import constants

class DesignSpaceParams():
    """
    Parent class that describes a common DesginSpaceParams.

    ...

    Attributes
    ----------
    circuit_type : str
        Circuit type constant. ex ( LOW_POWER, HIGH_PERFORMANCE )
    operation : str
        Circuit arithmetic operation ex ( ADDER, SUBSTRACTOR, MULTIPLER, DIVIDER )
    bitwidth : int
        Bitwidth of the circuit to be generated
    characteristic : str
        Charactheristic of the circuit to be minimized ex ( AREA, POWER, DELAY )
    error_metric : str
        Error metric used to select the circuits ( MED, WCE )
    threshold : float
        Maximun value aceptable for the given error metric
    """
    def __init__(self, database, circuit_type, circuit_operation, bitwidth, charactheristic, error_metric, threshold):
        self.database = database
        self.circuit_type = circuit_type
        self.circuit_operation = circuit_operation
        self.bitwidth = bitwidth
        self.charactheristic = charactheristic
        self.error_metric = error_metric
        self.threshold = threshold

    @property
    def bitwidth(self):
        return self._bitwidth

    @bitwidth.setter
    def bitwidth(self, value):
        if value < 0:
            raise Exception("min approx bits cannot be negative")
        else: 
            self._bitwidth = value

class  LowPowerDesignSpaceParams(DesignSpaceParams):
    """
    Class used to describe a LowPowerDesignSpaceParams, extends DesignSpaceParams and 
    adds parameters for approximate bits.

    ...

    Attributes
    ----------
    circuit_type : str
        Circuit type constant. ex (LOW_POWER, HIGH_PERFORMANCE)
    operation : str
        Circuit arithmetic operation ex (ADDER, SUBSTRACTOR, MULTIPLER, DIVIDER)
    bitwidth : int
        Bitwidth of the circuit to be generated
    characteristic : str
        Charactheristic of the circuit to be minimized ex ( AREA, POWER, DELAY )
    error_metric : str
        Error metric used to select the circuits ( MED, WCE )
    threshold : float
        Maximun value aceptable for the given error metric
    min_approx_bits: int
        Minimum  approximation bits to be simulated
    max_approx_bits: int
        Maximum  approximation bits to be simulated    
    """
    def __init__(
        self, 
        database,
        circuit_operation, 
        bitwidth, 
        charactheristic,
        error_metric, 
        threshold, 
        min_approx_bits, 
        max_approx_bits
    ):
        DesignSpaceParams.__init__(
            self,
            database,
            constants.LOW_POWER_CIRCUIT,
            circuit_operation,
            bitwidth,
            charactheristic,
            error_metric,
            threshold
        )
        self.__set_approx_bits(min_approx_bits, max_approx_bits)

    def __set_approx_bits(self, min_value, max_value):
        if min_value < 0:
            raise Exception("min approx bits cannot be negative")
        if max_value < 0:
            raise Exception("max approx bits cannot be negative")
        if self.bitwidth < min_value:
            raise Exception("min approx bits cannot be greater than the bitwidth")
        if self.bitwidth < max_value:
            raise Exception("max approx bits cannot be greater than the bitwidth")
        if min_value > max_value:
            raise Exception("max approx bits cannot be smaller than min approx bits")
        else: 
            self.min_approx_bits = min_value
            self.max_approx_bits = max_value


class  HighPerformanceDesignSpaceParams(DesignSpaceParams):

    def __init__(self, circuit_operation, bitwidth, charactheristic, error_metric, threshold, min_r, max_r, min_p, max_p):
        DesignSpaceParams.__init__(
            self,
            database,
            constants.HIGH_PERFORMANCE_CIRCUIT,
            circuit_operation,
            bitwidth,
            charactheristic,
            error_metric,
            threshold
        )
        self.min_r = min_r
        self.max_r = max_r
        self.min_p = min_p
        self.max_p = max_p
        

class DesignSpaceParamsBuilder():
    """
    Class used to implement builder pattern on DesignSpaceParams object
    """  
    
    @staticmethod
    def create_low_power_space_design_params(
        database,
        circuit_operation,
        bitwidth,
        charactheristic,
        error_metric,
        threshold,
        min_approx_bits,
        max_approx_bits
    ):
        """Static method create LowPowerDesignSpaceParams object

        
        Parameters
        ----------
        circuit_operation : str
            Circuit arithmetic operation ex (ADDER, SUBSTRACTOR, MULTIPLER, DIVIDER)
        bitwidth : int
            Bitwidth of the circuit to be generated
        characteristic : str
            Charactheristic of the circuit to be minimized ex ( AREA, POWER, DELAY )
        error_metric : str
            Error metric used to select the circuits ( MED, WCE )
        threshold : float
            Maximun value aceptable for the given error metric
        min_approx_bits: int
            Minimum  approximation bits to be simulated
        max_approx_bits: int
            Maximum  approximation bits to be simulated  
        """
    
        return LowPowerDesignSpaceParams(
            database,
            circuit_operation,
            bitwidth,
            charactheristic,
            error_metric,
            threshold,
            min_approx_bits,
            max_approx_bits
        )


    @staticmethod
    def create_high_performance_space_design_params(
        database,
        circuit_operation,
        bitwidth,
        charactheristic,
        error_metric,
        threshold,
        min_r,
        max_r,
        min_p,
        max_p
    ):
        return LowPowerDesignSpaceParams(
            database,
            circuit_operation,
            bitwidth,
            charactheristic,
            error_metric,
            threshold,
            min_approx_bits,
            max_approx_bits
        )