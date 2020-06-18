import pytest
from ui.ui import UI
from objects.design_space_params import DesignSpaceParamsBuilder
from objects.design_space_params import LowPowerDesignSpaceParams

# general builder tests 

def test_design_space_params_builder_invalid_circuit_type():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','8','-power','-t','0.25','-mina', '0', '-maxa', '4'])
    args.circuit_type = 'a'
    design_space_params_builder = DesignSpaceParamsBuilder()
    with pytest.raises(Exception):
        design_space_params = design_space_params_builder.create_design_space_params(args)

def test_design_space_params_builder_invalid_circuit_operation():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','8','-power','-t','0.25','-mina', '0', '-maxa', '4'])
    args.add = False
    design_space_params_builder = DesignSpaceParamsBuilder()
    with pytest.raises(Exception):
        design_space_params = design_space_params_builder.create_design_space_params(args)          

def test_design_space_params_builder_invalid_circuit_characteristic():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','8','-power','-t','0.25','-mina', '0', '-maxa', '4'])
    args.power = False
    design_space_params_builder = DesignSpaceParamsBuilder()
    with pytest.raises(Exception):
        design_space_params = design_space_params_builder.create_design_space_params(args)

# low power specific tests

def test_low_power_design_space_params():
    design_space_params = LowPowerDesignSpaceParams("ADDER", 8, "POWER", 0.25, 0, 4)
    assert design_space_params.circuit_type == "LOW_POWER"
    assert design_space_params.operation == "ADDER" #(SUB, MUL, DIV)
    assert design_space_params.bitwidth == 8
    assert design_space_params.charactheristic == "POWER"
    assert design_space_params.threshold == 0.25
    assert design_space_params.min_approx_bits == 0
    assert design_space_params.max_approx_bits == 4

def test_design_space_params_builder_low_power():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','8','-power','-t','0.25','-mina', '0', '-maxa', '4'])
    design_space_params_builder = DesignSpaceParamsBuilder()
    design_space_params = design_space_params_builder.create_design_space_params(args)
    assert design_space_params.circuit_type == "LOW_POWER"
    assert design_space_params.operation == "ADDER" #(SUB, MUL, DIV)
    assert design_space_params.bitwidth == 8
    assert design_space_params.charactheristic == "POWER"
    assert design_space_params.threshold == 0.25
    assert design_space_params.min_approx_bits == 0
    assert design_space_params.max_approx_bits == 4

def test_design_space_params_builder_low_power_negative_mina():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','8','-power','-t','0.25','-mina', '-1', '-maxa', '4'])
    design_space_params_builder = DesignSpaceParamsBuilder()
    with pytest.raises(Exception):
        design_space_params = design_space_params_builder.create_design_space_params(args)

def test_design_space_params_builder_low_power_negative_mixa():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','8','-power','-t','0.25','-mina', '0', '-maxa', '-4'])
    design_space_params_builder = DesignSpaceParamsBuilder()
    with pytest.raises(Exception):
        design_space_params = design_space_params_builder.create_design_space_params(args)

def test_design_space_params_builder_low_power_big_mina():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','8','-power','-t','0.25','-mina', '10', '-maxa', '4'])
    design_space_params_builder = DesignSpaceParamsBuilder()
    with pytest.raises(Exception):
        design_space_params = design_space_params_builder.create_design_space_params(args)

def test_design_space_params_builder_low_power_big_mixa():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','8','-power','-t','0.25','-mina', '0', '-maxa', '10'])
    design_space_params_builder = DesignSpaceParamsBuilder()
    with pytest.raises(Exception):
        design_space_params = design_space_params_builder.create_design_space_params(args)

def test_design_space_params_builder_low_power_invalid_mins():
    ui = UI()
    args = ui._UI__parse_input(['lp','-add','-bw','8','-power','-t','0.25','-mina', '5', '-maxa', '4'])
    design_space_params_builder = DesignSpaceParamsBuilder()
    with pytest.raises(Exception):
        design_space_params = design_space_params_builder.create_design_space_params(args)

# high performance specific tests