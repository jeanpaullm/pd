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

    def _find_file(self, rootdir, filename):
        '''
            Returns search for filename in rootdir, return path of file
            if not found returns None
        '''
        filepath = None
        for root, dir, files in os.walk(rootdir):
            if filename in files:
                filepath = os.path.join(root, filename)
                break
        return filepath

    def _execute_simulation(self, simulation):
        '''
            Executes simulation on AUGER, return false if failed.
        '''

        is_execution_successful = False

        command = [
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
            '-PMF'
        ]

        print(command)
        popen = subprocess.Popen(command, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()

        return True

    def _retrieve_simulation_characteristics(self, simulation):
        '''
            retrieves area, delay, power and pdp from simulation resume file, returns False if failed.
        '''

        resume_path = self._find_file(self.simulator_output_path,'RESUME.csv')

        #if unable to find it mark simulation as failed
        if resume_path is None:
            print("Error unable to find resume file")
            return False

        lineCount = 0
        dynamic_power = 0
        static_power = 0
        delay = 0
        area = 0

        with open(resume_path, newline='') as csvfile:
            resume = csv.reader(csvfile, delimiter=',')
            for row in resume:
                if lineCount == 2:
                    dynamic_power = float(re.findall('\d+\.\d+', row[0])[0])  #get dynamic power
                elif lineCount == 4:
                    static_power = float(re.findall('\d+\.\d+', row[0])[0])  #get cell leakage power
                elif lineCount == 8:
                    delay = float(re.findall('\d+\.\d+', row[0])[0]) # get delay results
                elif lineCount == 12:
                    area = float(re.findall('\d+\.\d+', row[0])[0]) # get area
                elif lineCount >=  13:
                    break    
                lineCount += 1

        #if line_count is smaller than 13 then the file was empty
        if lineCount >= 13:
            power = dynamic_power + (static_power * 10**-3) #multiply static power by 10^-3 to convert nW to uW
            simulation.power = power
            simulation.delay = delay
            simulation.area = area
            simulation.pdp = power * delay
            return True

        else:
            print("Error resume file empty")
            return False

    def _retrieve_simulation_errors(self, simulation):

        metrics_path = self._find_file(self.simulator_output_path,'METRICS.csv')

        #if unable to find it mark simulation as failed
        if metrics_path is None:
            print("Error unable to find metrics file")
            return False

        lineCount = 0
        errors = {}

        with open(metrics_path, newline='') as csvfile:
            metrics = csv.reader(csvfile, delimiter=',')
            for row in metrics:
                if lineCount >= 2: #on third line data starts 
                    errors[float(row[0])] = float(row[1])
                lineCount += 1

        #if line_count is cero then the file was empty
        if lineCount > 0:
            med = 0
            wce_value = 0
            for value in errors:               #iterate over errors dictionary
                med += value * errors[value]   #calculate med 
                if value > wce_value:          #check for wce
                    wce_value = value

            print(errors)
            print(med)
            print(errors[wce_value])

            simulation.med = med
            simulation.wce = errors[wce_value]

            print(simulation.med)
            print(simulation.wce)
            return True

        else:
            print("Error metrics file empty")
            return False

    def _cleanup(self):
        '''Removes generated simulation files '''
        shutil.rmtree(self.simulator_output_path, ignore_errors = True)

    def simulate(self, simulation):
        """Simulates and asigns charactheristics to given simulation, 
        returns true if succesful otherwise returns false.

        Parameters
        ----------
        simulation : Simulation
            Simulation object that contains the parameteres to be simulated.
        """

        is_simulation_successful = False

        if self._execute_simulation(simulation):
            is_simulation_successful = self._retrieve_simulation_characteristics(simulation) and self._retrieve_simulation_errors(simulation)
        self._cleanup()

        return is_simulation_successful