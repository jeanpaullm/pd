
class DesignSpaceParamsBuilder:
    """
    Class in charge of constructing a DesignSpaceParams object.

    ...

    Attributes
    ----------

    Methods
    -------
    create_design_space_params(args)
        Given an args object returns a DesignSpaceParams object.
    """

    def create_design_space_params(self, args):
        """Given an args object returns a DesignSpaceParams object.
        
        Auxiliary private methods converts args to constants

        Parameters
        ----------
        args : Args
            Parsed args from input

        Raises
        ------
        Exception
            If invalid circuit type, operation or characteristic.
        """
        if args.circuit_type == 'lp':
            return LowPowerDesignSpaceParams(
                self.__operation_to_const(args),
                args.bitwidth,
                self.__characteristic_to_const(args),
                args.threshold,
                args.mina,
                args.maxa)
        if args.circuit_type == 'hp':
            return HighPerformanceDesignSpaceParams(
                self.__operation_to_const(args),
                args.bitwidth,
                self.__characteristic_to_const(args),
                args.threshold,
                args.minp,
                args.maxp,
                args.minr,
                args.maxr)
        else:
            raise Exception("Invalid circuit type: " + args.circuit_type)

    def __operation_to_const(self, args):
        if args.add:
            return 'ADDER'
        elif operation.sub:
            return 'SUBSTRACTOR'
        elif operation.mul:
            return 'MULTIPLIER'
        elif operation.div:
            return 'DIVIDER'
        else:
            raise Exception("Invalid circuit type operation: No operation was specified")

    def __characteristic_to_const(self, args):
        if args.area:
            return 'AREA'
        elif args.delay:
            return 'DELAY'
        elif args.power:
            return 'POWER'
        else:
            raise Exception("Invalid circuit characteristic: No characteristic was specified")

    

class DesignSpaceParams:
    """
    Parent class that describes a common DesginSpaceParams.

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
        Charactheristic of the circuit to be explored ex ( AREA, POWER, DELAY)
    threshold : float
        Minimum value acceptable for the characteristic
    """
    def __init__(self, circuit_type, operation, bitwidth, charactheristic, threshold):
        self.circuit_type = circuit_type
        self.operation = operation
        self.bitwidth = bitwidth
        self.charactheristic = charactheristic
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
        Charactheristic of the circuit to be explored ex ( AREA, POWER, DELAY)
    threshold : float
        Minimum value acceptable for the characteristic
    min_approx_bits: int
        Minimum  approximation bits to be simulated
    max_approx_bits: int
        Maximum  approximation bits to be simulated    
    """
    def __init__(self, operation, bitwidth, charactheristic, threshold, min_approx_bits, max_approx_bits):
        DesignSpaceParams.__init__(self, "LOW_POWER", operation, bitwidth, charactheristic, threshold)
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

    def __init__(self, circuit_type, operation, bitwidth, charactheristic, threshold, min_r, max_r, min_p, max_p):
        DesignSpaceParams.__init__(self, "HIGH_PERFORMANCE", operation, bitwidth, charactheristic, threshold)
        self.min_p = minApproxBits
        self.maxApproxBits = maxApproxBits