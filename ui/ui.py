import argparse #parse console input

class UI:
    """Class used to abstract the UI layer, it deals with the parsing and validating 
    the data entered by the user in console, as well as plotting the end results.
    
     ...

    Attributes
    ----------
    logic: Logic
        Logic object that abstracts the logic layer

    Methods
    -------
    set_logic(args)

    parse_input(args)
        Parses the input from the user taken from console

    """


    def set_logic(self, logic):
        self.logic = logic



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

        #threshold
        parser_high_performance.add_argument('-t', '--threshold', type = float, required = True, help = 'minimum threshold of the selected characteristic')

        #simulation limits
        parser_high_performance.add_argument('-minr', type = int, required = True, help = 'minimum aproximated bits, default 0')
        parser_high_performance.add_argument('-maxr', type = int, required = True, help = 'maximum aproximated bits, default bitwidth')
        parser_high_performance.add_argument('-minp', type = int, required = True, help = 'minimum aproximated bits, default 0')
        parser_high_performance.add_argument('-maxp', type = int, required = True, help = 'maximum aproximated bits, default bitwidth')

        return parser.parse_args(args)    