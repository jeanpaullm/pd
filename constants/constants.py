#circuit type

LOW_POWER_CIRCUIT = "low_power"
HIGH_PERFORMANCE_CIRCUIT = "high_performance"


# circuit operation

ADDER      = "adder"
#SUBSTRACTOR = "substractor"
DIVIDER    = "divider"
MULTIPLIER = "multipler"

# characteristics
AREA  = "area"
DELAY = "delay"
POWER = "power"
PDP   = "pdp"

# simulation type

GENERATION = "-gen"
SIMULATION = "-sim"
VALIDATION = "-val"
SYNTHESIS = "-syn"
POST_SYNTHESYS = "-psy"

LOW_POWER_ADDERS = ["AFA1", "AMA1", "AMA2",
                    "AMA3", "AMA4", "AMA5",
                    "AXA1", "AXA2", "AXA3",
                    "VAXA", "LOA", "TGA1",
                    "TGA2", "InXA1", "InXA2",
                    "InXA3", "CFA"]

COMMANDS = {
    ADDER: "-a",
    MULTIPLIER: "-m",
    DIVIDER: "-d",
}