import pytest
from constants import constants
from objects.design_space_params import DesignSpaceParamsBuilder, LowPowerDesignSpaceParams


# low power specific tests
def test_low_power_design_space_params():
    design_space_params = DesignSpaceParamsBuilder.create_low_power_space_design_params(constants.ADDER, 8, constants.POWER, 0.25, 0, 4)
    assert design_space_params.circuit_type == constants.LOW_POWER_CIRCUIT
    assert design_space_params.circuit_operation == constants.ADDER #(SUB, MUL, DIV)
    assert design_space_params.bitwidth == 8
    assert design_space_params.charactheristic == constants.POWER
    assert design_space_params.threshold == 0.25
    assert design_space_params.min_approx_bits == 0
    assert design_space_params.max_approx_bits == 4