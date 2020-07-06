import configparser #to read config file
import subprocess #for executing simulations
import csv #csv manipulation
import os# checking if file exists
import shutil #delete output
import re #managing regex
from constants import constants

class Simulator():
    ''' On initialization gets output path, if unable to find it
        raises error
    '''
    def __init__(self):
        self.simulator_output_path = self._get_simulator_output_path()


    def _get_simulator_output_path(self):
        """Gets the output path defined in the config.cfg file.

        If the argument `sound` isn't passed in, the default Animal
        sound is used.


        Raises
        ------
        Error
            If config.cfg not pressent or unable to obtainn FilesPath from it.
        """

        configParser = configparser.RawConfigParser()
        outputPath = None
        if not configParser.read('./config.cfg'):
            raise Exception('Error: Unable to open config.cfg, file missing.')
        else:
            outputPath = configParser.get('AAUG setup','FilesPath')
        
        if outputPath is None:
            raise Exception('Error: Unable to obtain FilesPath fom config.cfg.')
        else:
            return outputPath
        

    def simulate(self, simulation):
        """Simulates the given asign simulation charactheristics to given simulation, 
        returns true if succesful otherwise returns false.

        Parameters
        ----------
        simulation : Simulation
            Simulation object that contains the parameteres to be simulated.
        """

        print(
            './AUGER',
            constants.COMMANDS[simulation.circuit_operation],
            simulation.approximation_method,
            '-bw',
            str(simulation.bitwidth),
            '-l',
            str(simulation.approximate_bits),
            simulation.simulation_type,
            '-rand',
            '-c',
            str(simulation.number_of_validations),
            '-ER')


        popen = subprocess.Popen([
            './AUGER',
            constants.COMMANDS[simulation.circuit_operation],
            simulation.approximation_method,
            '-bw',
            str(simulation.bitwidth),
            '-l',
            str(simulation.approximate_bits),
            simulation.simulation_type,
            '-rand',
            '-c',
            str(simulation.number_of_validations),
            '-ER'
        ], stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()

        resume_path = None
        filename = 'RESUME.csv'
        for root, dir, files in os.walk(self.simulator_output_path):
            if filename in files:
                resume_path = os.path.join(root, filename)
            break
    
        if resume_path is None:
            return False

        else:
            resume = csv.reader(open(resume_path, newline=''), delimiter=',')
            lineCount = 0
            power = 0
            delay = 0
            area = 0
            for row in resume:
                if lineCount == 2:
                    power = float(re.findall('\d+\.\d+', row[0])[0])  #get dynamic power
                elif lineCount == 4:
                    power += float(re.findall('\d+\.\d+', row[0])[0]) * 10**-3 #get cell leakage power, multiply by 10^-3 to convert nW to uW
                elif lineCount == 8:
                    delay = float(re.findall('\d+\.\d+', row[0])[0]) # get delay results
                elif lineCount == 12:
                    area = float(re.findall('\d+\.\d+', row[0])[0]) # get area
                elif lineCount >=  13:
                    break    
                lineCount += 1

            simulation.power = power
            simulation.delay = delay
            simulation.area = area

        
        #falta obtener errores

        # removes generated simulation files
        # creates 
        shutil.rmtree(self.simulator_output_path, ignore_errors = True) 

        return True