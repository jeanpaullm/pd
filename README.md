# Approximate Arithmetic Circuits Design Space Exploration.

This tool automates the generation and exploration of aproximate arithmetic circuits

## Dependencies

* Python3 >= 3.6.8
* Mathplotlib >= 3.2.2
* Synopsys 2017
* Modelsim >= 10.2
* Quetasim >= 10.2

## Installation

To create the AUGER binaries execute

```bash
make
```

## Usage

Note: As this tool uses AUGER to calculate the characteristics of the circuits Modelsim, Quetasim and Synopsis must be executed first.

```bash
python3 main.py [-h] [-nt] [-ndb] lp (-add | -mul | -div) -bw BITWIDTH (-area | -delay | -power | -pdp) (-med | -wce) [-t THRESHOLD] [-mina MINA] [-maxa MAXA]
```

* -h, --help:  shows help message and exit
* -nt: Executes without threading. Threads on by default
* -ndb: Executes all the design space, does not retrieve data from old simulations. Searching in database on by default
* lp: Execute low power circuit design space
* (-add | -mul | -div): Arithmetic operation to explore design space
* -bw, --bitwidth: BITWIDTH bitwidth of the arithmetic circuit
* (-area | -delay | -power | -pdp): Design characteristic to minimize
* (-med | -wce): Error metric used to compare the cricuits
* -t THRESHOLD: Maximum value of the error metric acepted
* -mina MINA:  minimum approximate bits.
* -maxa MAXA: maximum approximate bits.

### Example 

```bash
python3 main.py -ndb lp -add -bw 32 -area -wce -t 2.5 -mina 1 -maxa 16
```

## Known Bugs

* A no threaded execution must be done before executing a threaded one.
