import argparse #parse console input
from logic.logic import Logic
from constants import constants
from objects.design_space_params import DesignSpaceParamsBuilder

class UI:
    """Class used to abstract the UI layer, it deals with the parsing and validating 
    the data entered by the user in console, as well as plotting the end results.
    
     ...

    Attributes
    ----------
    logic: Logic
        Logic object that abstracts the logic layer
    """


    def set_logic(self, logic):
        self.logic = logic

    def start_exploration(self, args):
        """Initiazlizes the tool execution. 

        Parses the input from the user, validates it and converts it into 
        a DesignSpaceParams object that is passed to the Logic that by means
        of the explore_design_space

        Parameters
        ----------
        args : str[]
            list of commands entered from the user in console

        """

        parsed_args = self.__parse_input(args)
        design_space_params = self.__create_design_space_params(parsed_args)
        self.logic.set_design_space_params(design_space_params)
        self.logic.init()

    #TODO
    def plot():
        pass    

    def __parse_input(self, args):
        """ Parses options entered by the user in console.

        It makes sure all the options are entered by the user 
        otherwise an exception is raised.

        Parameters
        ----------
        args : argv
            input from console

        Raises
        ------
        SystemExit
            If a required field is not entered
            
        """

        parser = argparse.ArgumentParser(description = 'This tool is used to explore the design space of aproximate aritmetic circuits') # Description?

        subparsers = parser.add_subparsers(dest='circuit_type', required=True)

        ## low power circuit subparser ##
        parser_low_power = subparsers.add_parser('lp', help = 'Creates low power circuits design space')

        #aritmetic operation selection
        operation_group =  parser_low_power.add_mutually_exclusive_group(required=True)
        operation_group.add_argument('-add', action = 'store_true')
        operation_group.add_argument('-sub', action = 'store_true')
        operation_group.add_argument('-mul', action = 'store_true')
        operation_group.add_argument('-div', action = 'store_true')

        #especify operation bit width
        parser_low_power.add_argument('-bw', '--bitwidth', type = int, required = True, help = 'bitwitdth of the aritmetic circuit')

        #especify caractheristics
        charactheristics_group =  parser_low_power.add_mutually_exclusive_group(required=True)
        charactheristics_group.add_argument('-area', action = 'store_true')
        charactheristics_group.add_argument('-delay', action = 'store_true')
        charactheristics_group.add_argument('-power', action = 'store_true')
        charactheristics_group.add_argument('-pdp', action = 'store_true')

        #threshold
        parser_low_power.add_argument('-t', '--threshold', type = float, required = True, help = 'minimum threshold of the selected characteristic')

        #simulation limits
        parser_low_power.add_argument('-mina', type = int, required = True, help = 'minimum aproximated bits, default 0')
        parser_low_power.add_argument('-maxa', type = int, required = True, help = 'maximum aproximated bits, default bitwidth')
        

        ## high performance circuit subparser ##
        parser_high_performance = subparsers.add_parser('hp', help = 'Creates high performance circuits design space')

        #aritmetic operation selection
        operation_group =  parser_high_performance.add_mutually_exclusive_group(required=True)
        operation_group.add_argument('-add', action = 'store_true')
        operation_group.add_argument('-sub', action = 'store_true')
        operation_group.add_argument('-mul', action = 'store_true')
        operation_group.add_argument('-div', action = 'store_true')

        #especify operation bit width
        parser_high_performance.add_argument('-bw', '--bitwidth', type = int, required = True, help = 'bitwitdth of the aritmetic circuit')

        #especify caractheristics
        charactheristics_group = parser_high_performance.add_mutually_exclusive_group(required=True)
        charactheristics_group.add_argument('-area', action = 'store_true')
        charactheristics_group.add_argument('-delay', action = 'store_true')
        charactheristics_group.add_argument('-power', action = 'store_true')
        charactheristics_group.add_argument('-pdp', action = 'store_true')

        #threshold
        parser_high_performance.add_argument('-t', '--threshold', type = float, required = True, help = 'minimum threshold of the selected characteristic')

        #simulation limits
        parser_high_performance.add_argument('-minr', type = int, required = True, help = 'minimum aproximated bits, default 0')
        parser_high_performance.add_argument('-maxr', type = int, required = True, help = 'maximum aproximated bits, default bitwidth')
        parser_high_performance.add_argument('-minp', type = int, required = True, help = 'minimum aproximated bits, default 0')
        parser_high_performance.add_argument('-maxp', type = int, required = True, help = 'maximum aproximated bits, default bitwidth')

        return parser.parse_args(args)    

    def __create_design_space_params(self, parsed_args):
        """Given an args object returns a DesignSpaceParams object.

        Parameters
        ----------
        parsed_args : ParsedArgs
            Parsed args from input

        Raises
        ------
        Exception
            If invalid circuit type
        """
        if parsed_args.circuit_type == 'lp':
            return DesignSpaceParamsBuilder.create_low_power_space_design_params(
                self.__parsed_args_to_const_circuit_operation(parsed_args),
                parsed_args.bitwidth,
                self.__parsed_args_to_const_characteristic(parsed_args),
                parsed_args.threshold,
                parsed_args.mina,
                parsed_args.maxa)

        if parsed_args.circuit_type == 'hp':
            return DesignSpaceParamsBuilder.create_high_performance_space_design_params(
                self.__parsed_args_to_const_circuit_operation(parsed_args),
                parsed_args.bitwidth,
                self.__parsed_args_to_const_characteristic(parsed_args),
                parsed_args.threshold,
                parsed_args.minp,
                parsed_args.maxp,
                parsed_args.minr,
                parsed_args.maxr
            )
        else:
            raise Exception("Invalid circuit type: " + parsed_args.circuit_type)

    def __parsed_args_to_const_circuit_operation(self, parsed_args):
        """Returns contant circuit operation string corresponding to the given parsed args

        Parameters
        ----------
        parsed_args : ParsedArgs
            Parsed args from input

        Raises
        ------
        Exception
            If invalid circuit operation.
        """

        if parsed_args.add:
            return constants.ADDER
        elif parsed_args.sub:
            return constants.SUBSTRACTOR
        elif parsed_args.mul:
            return constants.MULTIPLIER
        elif parsed_args.div:
            return constants.DIVIDER
        else:
            raise Exception("Invalid circuit operation: No circuit operation was specified")

    def __parsed_args_to_const_characteristic(self, parsed_args):
        """Returns contant characteristic string corresponding to the given parsed args

        Parameters
        ----------
        parsed_args : ParsedArgs
            Parsed args from input

        Raises
        ------
        Exception
            If invalid circuit operation.
        """

        if parsed_args.area:
            return constants.AREA
        elif parsed_args.delay:
            return constants.DELAY
        elif parsed_args.power:
            return constants.POWER
        elif parsed_args.pdp:
            return constants.PDP
        else:
            raise Exception("Invalid circuit characteristic: No circuit characteristic to be optimized was specified")